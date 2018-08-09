use lib "/local/git/mingit/current/lib";

use strict;
use Carp;
use SendMail;
use GitCDETS qw( getRepoHash );
use IO::Select;
use IO::Socket::INET;

my $u             = "missing";
my $p             = "missing";
my %info          = ();
my $last          = $ARGV[0];
my $next          = $ARGV[1];
my $head          = $ARGV[2];
my $id_ref        = -1;
my $id_num        = 0;
my $verify_id     = -1;
my $content       = '';
my $subject       = '';
my @tmp_arr       = ();
my $u_p_valid     = 0;
my $save_rc       = 0;
my $hostname      = `hostname`;
my $curr_branch   = '';
my $email_contact = 'kalathk@cisco.com';
my $attach_option = 0;

## 0 = no testtrack validation, 1 = testtrack validation ##
my $override_ttrack_validation = 1;

$head =~ m{refs/heads/([a-zA-Z0-9]+)};
$curr_branch = $1;

my $GITCMD;
if ( -e "/usr/cisco/bin/git" ) {
          $GITCMD = "/usr/cisco/bin/git";
  }
  else {
          $GITCMD = `which git`;
}

my @revlist;
if ( $last eq "0000000000000000000000000000000000000000"){
  @revlist= `$GITCMD rev-list $next | head -n 1`;
}
else {
        @revlist = `$GITCMD rev-list $last..$next`;
}

foreach my $commit ( @revlist ) {

  chomp($commit);
  my $commentsCMD = `$GITCMD log -p -1 $commit`;

  ### option in comment to attach a file to defect number ###
  if ( $commentsCMD =~ /attach=(1)/m ) {
    $attach_option = $1;
  }

  ### verify user and password are in git comment ###
  if ( $override_ttrack_validation ) {
     if ( $commentsCMD =~ /u=([a-zA-Z0-9]+)/m ) {
       $u = $1;
     }
     else {
       $u_p_valid = 1;
     }

     if ( $commentsCMD =~ /p=([a-zA-Z0-9]+)/m ) {
       $p = $1;
     }
     else {
       $u_p_valid = 1;
    }
 }

  # Grab repository.settings info
  my $repoSettings = getRepoHash();

  my $DefectSystemTTrack = (defined $repoSettings->{defect_system})          ? ( $repoSettings->{defect_system} eq "testtrack" ) : 0;
  my $DefectRequired     = (defined $repoSettings->{defect_required})        ? $repoSettings->{defect_required} : 0;
  my $TTrackAttachDiff   = (defined $repoSettings->{testtrack_attach_diff})  ? $repoSettings->{testtrack_attach_diff} : 1;
  my $TTrackBlockCommit  = (defined $repoSettings->{testtrack_block_commit}) ? $repoSettings->{testtrack_block_commit} : 0;

  if ( $DefectSystemTTrack ) {
    my $gitdiff = "BRANCH: $curr_branch\n";
    $gitdiff .= `$GITCMD  show -m --name-status $commit`;
    $gitdiff =~ s/\t/    /g;

    my $infoSubjectID = "Invalid TestTrack Defect Number";
    my $invalidTrackID = '';

    $verify_id = valid_format_in_comment($commit,$commentsCMD, \$id_ref);
    $id_num = $id_ref;

    if ( $verify_id == 1) {
       $invalidTrackID = "Git server $hostname format is invalid for TestTrack Defect number in comment\n\n$gitdiff\n";
    }

    if ( $u_p_valid == 1 ) {
       $verify_id = 1;
       $invalidTrackID = "Missing testTrack user name or user password.\n This information must be in yourgit comment.\n";
       $invalidTrackID .= "Please input your username and password in the commit message.\"\n\n $gitdiff\n\n";
       $infoSubjectID = "Missing testTrack user name or password";
    }

    $id_ref = $id_ref . " " . $u . " " . $p;
    if ( $override_ttrack_validation ) {
       if ( $verify_id == 0 ) {

          $verify_id = verify_TTrack_id( $id_ref );

          if ( $verify_id == 4 ) {
            $invalidTrackID = "A timeout issue has occurred with communication to TestTrack.\n";
            $invalidTrackID .= "This could be a temporary issue. Please try git push again.\n\n";
            $invalidTrackID .= "If timeout issues persist please contact $email_contact.\n";
            $infoSubjectID = "Communication to TestTrack timed out";
          }

          if ( $verify_id  == 2 ) {
            $invalidTrackID = "TestTrack Defect number $id_num not found in TestTrack Database\n\n $gitdiff
\n";
          }

          if ( $verify_id == 3 ) {
            $invalidTrackID = "Failed Login to the TestTrack server.\n";
            $invalidTrackID .= "The username or password you entered in not valid or you do not\n";
            $invalidTrackID .= "have the correct security permissions to login.\n\n $gitdiff\n\n";
            $invalidTrackID .= "If Login problems persist please contact $email_contact\n\n";

            $infoSubjectID = "Invalid username or password in commit comment";
          }
       }
    }

     if ( $verify_id ) {
       if ( $DefectRequired ) {
         $verify_id = 1 if ( $TTrackBlockCommit );

         # email user saying invalid CDETS is
         $info{sender} = "gitadmin";
         $info{to} = $ENV{USER};

         $info{subject} = $infoSubjectID;
         $info{subject} =~ s/--/\//;


         $content .=  $invalidTrackID;
         if ( $verify_id != 4 ) {
           $content .=  "You can update your comment using:\n";
           $content .=  '  git commit --amend -m "TT xxxx u=valid_user p=valid_password commit message "' ."\n";
           $content .=  "  Try your git push again\n\n";
         }

         # Print local user messageprint "$content";
          print "$content\n";

         #$content = $content . $gitdiff;
         $info{content} = $content;
         email_user(\%info);

       }

       last;
     }
     else {
        if ( $override_ttrack_validation ) {

           if ( $attach_option == 0 ) {
              $save_rc = attach_diff_to_id( $gitdiff, $attach_option );
           }
           else {
              if ( $TTrackAttachDiff || $attach_option ) {
                 $save_rc = attach_diff_to_id( $gitdiff, $attach_option );
              }
           }

              if ( $save_rc == 1 ) {
                 $content  = "ERROR: Failed to attach to the TestTrack Defect Number.\n\n";
                 $content .= "This is usually due to a save communication error to the TestTrack database\n";
                 $content .= "This could be a temporary issue. Your git push will need to be tried again.\n\n";
                 $content .= "If attachment problems persist please contact $email_contact\n\n";
                 $content .= "$gitdiff";
                 $verify_id = 1;
                 print "$content";
              }

              if ( $save_rc == 2 ) {
                 $content  =  "ERROR: Failed to attach to the TestTrack Defect Number.\n\n";
                 $content .=  "This is usually due to the DATE ENTERED field checkbox not being checked for this defect.\n";
                 $content .=  "Please verify this checkbox is selected before the next commit to this defect.\n\n";
                 $content .=  "Then retry your git push command.\n\n";
                 $content .=  "If attachment problems persist please contact $email_contact\n\n";
                 $content .=  "$gitdiff";
                 $verify_id = 1;
                 print "$content";
              }

              if ( $save_rc == 3 ) {
                 $content  =  "ERROR: Failed to attach to the TestTrack Defect Number.\n";
                 $content .=  "This is probably due to the defect being locked for editing.\n";
                 $content .=  "Please verify this record has been unlocked before doing any more commits.\n\n";
                 $content .=  "Then retry your git push command.\n\n";
                 $content .=  "If attachment problems persist please contact $email_contact\n\n";
                 $content .=  "$gitdiff";
                 $verify_id = 1;
                 print "$content";
              }

              if ( $save_rc == 4 ) {
                $content = "A timeout issue has occurred with communication to TestTrack.\n";
                $content .= "This could be a temporary issue. Please try git push again.\n\n";
                $content .= "If timeout issues persist please contact $email_contact.\n";
                print "$content";
                $verify_id = 1;
              }

              if ( $save_rc != 0 ) {
                 $info{sender} = "gitadmin";
                 $info{to} = $ENV{USER};
                 $info{subject} = "An error occurred when attaching the code diff to TT $id_num";
                 $info{content} = $content;
                 email_user(\%info);
              }

              if ( $save_rc == 0 ) {
                print "Git push has completed\n";
              }

       }

      if ( $save_rc == 0 ) {
         print "Changes committed to Repository\n";
      }

    }


  } # end defectsystemtrack if

} # end foreach

exit( $verify_id );


###########################################################################

sub verify_TTrack_id {
  my ( $defect_id )  = @_;
  my $ttrack_rsp = -1;
  my $socket     = -1;
  my $ret_data   = -1;
  my $defect_num = 0;
  my $timeout    = 30;
  my $rc = -1;

  $| = 1;     #flush every write

  my $sock_err_msg = "\n*****************************************************\n" .
                     "Error in Socket Creation to TestTrack Proxy Server.\n" .
                     "Test Track Listener could be down on the Proxy Server.\n" .
                     "Verify with cisco.com if listener is\n" .
                     "running.";


  $socket = IO::Socket::INET->new(
                      'PeerHost' => '',
                      'PeerPort' => '2200',
                      'Proto'    => 'tcp', )  ||  croak("$sock_err_msg\n");

  my $sel_sock = IO::Select->new( $socket )  ||  croak("Failed to create Select object\n");
  my $write_server = 0;
  my $read_server  = 0;


  $defect_id =~ /^(\d+)/;
  $defect_num = $1;

  print "TCP connection to TestTrack Proxy Server: Success\n";
  print "Verify valid Defect Number: $defect_num\n";

  #### timeout if not able to write ###
  if ( my @sock_write = $sel_sock->can_write( $timeout )) {
    $write_server = shift(@sock_write);

  print $write_server "$defect_id\n";
  }
  else {
     print "Timed out on write to TestTrack\n";
     $rc = 4;
  }

  #### timeout if not able to read ###
  if ( my @socks = $sel_sock->can_read( $timeout )) {
    $read_server = shift(@socks);

    #  receive response from server #
    $ret_data = <$read_server>;
  }
  else {
     print "Timed out on read response from TestTrack\n";
     $rc = 4;
  }

  if ( !defined( $ret_data ) ) {
    print "No data returned from server while verifying Defect number\n";
  }

  $socket->close()    ||  warn("\tFailed to cleanly close the client socket to proxy server\n");

  if ( $ret_data == 0 ) {
    $rc = 0;
  }
  elsif ( $ret_data == 3 ) {
    $rc = 3;
  }
  elsif ( $ret_data == 1 ) {
    $rc = 2;
  }

  return( $rc );
}


sub attach_diff_to_id {
  my( $diff_msg, $do_attach ) = @_;
  my( $socket )    = -1;
  my( $ret_data)   = -1;
  my( $rc )        = -1;
  my( $timeout)    = 30;

  $| = 1;     #flush every write

  my $sock_err_msg = "\n*****************************************************\n" .
                     "Error in Socket Creation to TestTrack Proxy Server.\n" .
                     "Test Track Listener could be down on the Proxy Server.\n" .
                     "Verify with John Bucy Jr.(bucyj\@cisco.com if listener is\n" .
                     "running.";


  $socket = IO::Socket::INET->new(
                      'PeerHost' => '',
                      'PeerPort' => '2200',
                      'Proto'    => 'tcp', )  ||  croak("$sock_err_msg\n");


  my $sel_sock = IO::Select->new( $socket )  ||  croak("Failed to create Select object\n");
  my $write_server = 0;
  my $read_server  = 0;

  $diff_msg =~ s/\n/X/g;
  $diff_msg =~ /(commit)\s([a-z0-9]{13})/;
  my $filename = "$1_$2.txt";

  if ( $do_attach ) {
    print "Attaching commit diff message $filename \n\n";
  }

  #### timeout if not able to write ###
  if ( my @sock_write = $sel_sock->can_write( $timeout )) {
    $write_server = shift(@sock_write);
    print $write_server "$diff_msg\n";
  }
  else {
     print "Timed out on write to TestTrack.\n";
     $rc = 4;
  }

  #### timeout if not able to read ###
  if ( my @socks = $sel_sock->can_read( $timeout )) {
    $read_server = shift(@socks);

    #  receive response from server #
    $ret_data = <$read_server>;
  }
  else {
     print "Timed out on read response from TestTrack\n";
     $rc = 4;
  }

  $socket->close()    ||  warn("\tFailed to cleanly close the client socket to proxy server\n");

  #### need to verify a value returned, Listener process could have
  #### stopped between git pushing and receiving a value from listener.
  if ( !defined($ret_data) ) {
     print "No response from server during the attachment to defect number\n";
     return 1;
  }

  if ( $ret_data == 0 ) {
    ### everything is ok
    $rc = 0;
  }
  elsif ( $ret_data == 2 ) {
    ###  there was an empty date tag
    $rc = 2;
  }
  elsif ( $ret_data == 3 ) {
    ### defect is locked by another user
    $rc = 3;
  }
  else {
    ###  unknown type soap error
    $rc = 1;
  }

  return( $rc );
}


sub valid_format_in_comment {
 my( $com_key, $comments, $ref_id ) = @_;
 my $found_key = 0;

 my @commitArr = split(/\n/,$comments);
   my $foundkey = 0;

   for my $line ( @commitArr ) {
      if ( $line =~ /\bTT\b\s{1,3}(\d+)/ ) {
          ${$ref_id} = $1;
          $found_key = 1;
         last;
      }
   }

   if ( $found_key == 1 ) {
     return(0);
   }
   else {
    return(1);
   }
}

