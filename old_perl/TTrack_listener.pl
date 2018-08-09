#!c:/Perl64/bin/perl

###################################################################################
#  TTrack_listener.pl - This script sits on the windows server to give            #
#                       access to the TestTrack system. This script will listen   #
#                       on 10.83.105.103:2200 for any incoming hook calls.        #
#                       The hook sends the Defect number, the listener will       #
#                       receive the number and pass it to the SOAP call to        #
#                       validate the Test Track number.                           #
#                                                                                 #
#  Input:                                                                         #
#        variable $defect_number - holds the testTrack number or                  #
#                                  the git diff comment                           #
#                                                                                 #
#  Output:                                                                        #
#        variable $save_ok -   0 for valid, no issues                             #
#                              2 soap issue, checkbox not checked,date missing    #
#                              3 edit in client and edit by SOAP API not allowed  #
#                              1 unknown soap soap issue                          #
###################################################################################

use strict;

use Carp;
use ttsoapcgi;
use SOAP::Lite;
use MIME::Base64;
use IO::Socket::INET;
use POSIX qw( strftime );
#use SOAP::Lite +trace => 'debug';

my $rsp            = -1;
my $data           = 0;
my $sock           = 0;
my $listener       = 0;
my $client_address = 0;
my $client_port    = 0;
my $cookie         = 0;
my $ttcookie       = 0;
my $xml_logon      = '';
my $defect_result  = 0;
my $defect_number  = 0;
my $hook_msg       = '';
my $logoff_ttrack  = 1;
my $save_ok        = 1;
my $diff_msg       = '';
my $save_defectnum = 0;
my $project_logon_xml = '';
my $datetime = strftime('%Y-%m-%d-%H:%M:%S', localtime() );
my $soap_user = '';
my $soap_pw   = '';

###############   data for access to TestTrack Server ######
my $database  = "DirecTV Headend";
#my $database  = "DirecTV Sandbox";
############################################################

##############   Setup SOAP objects ########################
my($soap_logon) = SOAP::Lite->new()   ||  croak("\tfailed to create SOAP logon object...\n");
my $soap_tt = ttsoapcgi->ttpro->new() ||  croak("\tfailed to create TTSOAPCGI object...\n");

$soap_logon->proxy('http://ttr-app-001-p.cisco.com:80/scripts/ttsoapcgi.exe');
$soap_logon->ns('urn:testtrack-interface');
$soap_logon->serializer->register_ns("http://schemas.xmlsoap.org/soap/envelope/","SOAP-ENV");
$soap_logon->serializer->register_ns("http://schemas.xmlsoap.org/wsdl/mime/","MIME");
$soap_logon->serializer->register_ns("http://schemas.xmlsoap.org/wsdl/soap/","SOAP");
$soap_logon->serializer->register_ns("urn:testtrack-interface","ttns");
$soap_logon->serializer->register_ns("http://www.w3.org/2001/XMLSchema-instance","xsi");
$soap_logon->serializer->register_ns("http://schemas.xmlsoap.org/soap/encoding/","SOAP-ENC");
$soap_logon->serializer->register_ns("http://schemas.xmlsoap.org/wsdl/","WSDL");
$soap_logon->serializer->register_ns("urn:testtrack-interface","tns");
$soap_logon->serializer->register_ns("http://www.w3.org/2001/XMLSchema","xsd");
$soap_logon->serializer->register_ns("http://schemas.xmlsoap.org/ws/2002/04/dime/wsdl/","DIME");

my $sock_error_msg = " Failed to create Listener on port:2200. TestTrack Defect\n" .
                     " Number cannot be verified until listener is started back up.\n" .
                     " --- Start listener on E: drive,  TTrack_listener.pl ---\n" .
                     "E:\\cmd /c start \"\" /min E:\\TTrack_listener.pl";

$| = 1;   # auto flush

######  Set up Socket Listener #####
$sock = new IO::Socket::INET (
        'LocalHost' => '',
        'LocalPort' => '2200',
        'Proto'     => 'tcp',
        'Listen'    => 50,
        'Reuse'     => 1,
)  ||   croak("$sock_error_msg\n");

print "Test Track Listener started on Windows Server... \n";
print "TestTrack Listener on port 2200: $datetime\n";

 while(1) {
    $rsp           = -1;
    $defect_number = 0;
    $ttcookie      = 0;

    $listener = $sock->accept();
    $client_address = $listener->peerhost();
    $client_port    = $listener->peerport();

    # print "Accepted New Client Connection from: $client_address:$client_port\n";

    $hook_msg = <$listener>;

    if ( $hook_msg =~ /^\d+/ ) {
      ($defect_number, $soap_user, $soap_pw) = split(/\s/,$hook_msg);
    }
    else {
       $defect_number = $hook_msg;
       $defect_number =~ s/u=[a-zA-Z1-9]+//;
       $defect_number =~ s/p=[a-zA-Z1-9]+//;
    }

    ##### Call ProjectLogon manually #####
    $soap_logon->on_action( sub {'urn:testtrack-interface#ProjectLogon'} );
    $project_logon_xml = "<pProj xsi:type=\"ttns:CProject\">" .
                         "<database><name xsi:type=\"xsd:string\">$database</name></database>" .
                         "<options SOAP-ENC:arrayType=\"ttns=CProjectDataOption[1]\" xsi:type=\"SOAP-ENC:Array\">" .
                         "<item xsi:type=\"ttns:CProjectDataOption\">" .
                         "<name xsi:type=\"xsd:string\">TestTrack Pro</name></item></options>" . 
                         "<servernumber xsi:type=\"xsd:int\">0</servernumber>" .
                         "</pProj><username xsi:type=\"xsd:string\">$soap_user</username>" .
                         "<password xsi:type=\"xsd:string\">$soap_pw</password>";

    $xml_logon = SOAP::Data->type( 'xml' => $project_logon_xml );
    $cookie = $soap_logon->call('ProjectLogon', $xml_logon );

    if ( $cookie->fault ) {
      print "Logon to the TestTrack server failed...\n";
      print "Access to the TestTrack SOAP API may be down...\n";
      print $cookie->faultstring();
      $rsp = 3;
    }
    else {
      $ttcookie = $cookie->result();
    }

   ##########   verify defect number here ###############
   if ( $defect_number !~ /commit/ ) {

      chomp($defect_number);
      print "Incoming Hook call with Defect Number: $defect_number\n";

      if ( $rsp != 3 ) {

         # TestTrack SOAP API from ttsoapcgi.pm #
         $defect_result = $soap_tt->getDefect( $ttcookie, $defect_number,'', 0 );

         # if defect number in TestTrack will return hash #
         if ( exists( $defect_result->{'defectnumber'} ) ) {
            $rsp = 0;

            $logoff_ttrack = $soap_tt->DatabaseLogoff( $ttcookie );

            if ( $logoff_ttrack != 0 ) {
              print "SOAP operation DatabaseLogoff failed to logoff cleanly for cookie: $ttcookie\n";
              print "This could limit the number of SOAP connections that are available.\n";
            }

         }
         else {
            $rsp = 1;

            $logoff_ttrack = $soap_tt->DatabaseLogoff( $ttcookie );
            if ( $logoff_ttrack != 0 ) {
              print "SOAP operation DatabaseLogoff failed to logoff cleanly for cookie: $ttcookie\n";
              print "This could limit the number of SOAP connections that are available.\n";
            }
         }
      }

    $save_defectnum = $defect_number;
    ##### return value from TestTrack Verification #####
    print $listener "$rsp\n";
  }

  ########################   save commit diff here #######################
  if ( $defect_number =~ /commit/ ) {
     $diff_msg = $defect_number;
     $diff_msg =~ s/X/\n/g;

     print "Incoming git diff attachment for Defect Number: $save_defectnum\n\n";
     $save_ok = save_commit( $soap_tt, $ttcookie, $save_defectnum, $diff_msg );

     $logoff_ttrack = $soap_tt->DatabaseLogoff( $ttcookie );
     if ( $logoff_ttrack != 0 ) {
        print "SOAP operation DatabaseLogoff failed to logoff cleanly for cookie: $ttcookie\n";
        print "This could limit the number of SOAP connections that are available.\n";
     }

     print $listener "$save_ok\n";
 }

}  # while loop

  $sock->close() ||  warn("\tFailed to close the TTrack listener cleanly....\n");
  exit(1);


########################################################################
#  will update later - This is a ugly subroutine. Seapine Testtrack
#  support will not help with their SOAP perl lib savecommit not working.
#  Had to manually create the SOAP message to keep project on track.
#  Works fine, git commit is being saved to the TestTrack defect system.
#########################################################################
sub save_commit {
   my( $soap_tt, $cookie, $defect_number, $diff_msg ) = @_;
   my $save_ok           = 1;
   my $save_xml          = '';
   my $save_result       = '';
   my $filename          = '';
   my $event_list        = '';
   my $cnt_events        = 0;
   my $author            = '';
   my $array_event       = 0;
   my $total_assigned_to = 0;
   my $array_size        = 0;
   my $attach_list       = '';
   my $xml_save          = '';
   my $cnt_attachments   = 0;
   my $total_reported_by = 0;
   my $do_attachment     = 0;
   my $fix_date = strftime('%Y-%m-%d',localtime() ) . "T" . strftime('%H:%M:%S', localtime() ) ;


   $diff_msg =~ /(commit)\s([a-z0-9]{13})/;
   $filename = "$1_$2.txt";

   if ( $diff_msg =~ /^Author:\s(\w+)\s(\w+)/m ) {
     $author = "$2, $1";
   }

   if ( $diff_msg =~ /attach=1/m ) {
     $do_attachment = 1;
   }

   $diff_msg =~ s/&/&amp\;/g;
   $diff_msg =~ s/>/&gt\;/g;
   $diff_msg =~ s/</&lt\;/g;

   $defect_result = $soap_tt->editDefect( $cookie, $defect_number,'', 'true' );
   if ( !defined($defect_result) ) {
      return( 3 );
   }

   # get the total reported records already in the defect
   $total_reported_by = scalar( @{$defect_result->{'reportedbylist'}} );

   if ( $do_attachment ) {
      ####### section for adding attachments to defect number #####
      if ( exists( $defect_result->{'reportedbylist'}->[0]->{'attachmentlist'} ) ) {
        $cnt_attachments = 0;
        $attach_list = '';

        
        # create current attachment list
        foreach my $attach_ref ( @{ $defect_result->{'reportedbylist'}->[0]->{'attachmentlist'}} ) {
           $attach_list .= "<item xsi:type=\"ttns:CFileAttachment\"SOAP-ENC:position=\"[$cnt_attachments]\">" .
                           "<m-pFileData>$attach_ref->{'m-pFileData'}</m-pFileData>" . 
                           "<m-strFileName>$attach_ref->{'m-strFileName'}</m-strFileName>" .
                           "<m-recordid>$attach_ref->{'m-recordid'}</m-recordid>" .
                           "<m-strArchiveName>$attach_ref->{'m-strArchiveName'}</m-strArchiveName>" .
                           "<m-strType>$attach_ref->{'m-strType'}</m-strType>" .
                           "<m-scriptOrder>$attach_ref->{'m-scriptOrder'}</m-scriptOrder></item>";
           ++$cnt_attachments;
        }

        # add the git diff to the end of the attachment list
        $array_size = 1 + $cnt_attachments;
        $attach_list .= "<item xsi:type=\"ttns:CFileAttachment\" SOAP-ENC:position=\"[$cnt_attachments]\">" .
                        "<m-pFileData>" . encode_base64($diff_msg, '') . "</m-pFileData>" .
                        "<m-strFileName>$filename</m-strFileName></item>";
     }
     else {
       $array_size = 1;
       $cnt_attachments = 0;
       $attach_list = "<item xsi:type=\"ttns:CFileAttachment\" SOAP-ENC:position=\"[$cnt_attachments]\">" .
                      "<m-pFileData> " . encode_base64($diff_msg, '') . "</m-pFileData>" .
                      "</m-pFileData><m-strFileName>$filename</m-strFileName></item>";
     }
   }
   ###################  end section for adding attachments                      #################

   ###################  section for adding git diff to events for defect number #################
   if ( exists( $defect_result->{'eventlist'} ) ) {
      $event_list = '';
      $cnt_events = 0;


      # create the current event list, then add git diff to end of list
      foreach my $eve_ref ( @{ $defect_result->{'eventlist'}} ) {

        $eve_ref->{'notes'} =~ s/&/&amp\;/g;
        $eve_ref->{'notes'} =~  s/>/&gt\;/g;
        $eve_ref->{'notes'} =~  s/</&lt\;/g;

        $eve_ref->{'resultingstate'} =~ s/&/&amp\;/g;
        $eve_ref->{'resultingstate'} =~  s/>/&gt\;/g;
        $eve_ref->{'resultingstate'} =~  s/</&lt\;/g;

        $event_list .= "<itemxsi:type=\"ttns:CEvent\"><recordid>$eve_ref->{'recordid'}</recordid><user>" .                                                                      "<xsi:type=\"ttns:CEvent\"><recordid>$eve_ref->{'recordid'}</recordid>" .
                       "<user>$eve_ref->{'user'}</user><date>$eve_ref->{'date'}</date><notes>$eve_ref->{'notes'}</notes>";

        $event_list .= "<eventaddorder>$eve_ref->{'eventaddorder'}</eventaddorder><name>$eve_ref->{'name'}</name>" .
                       "<parenteventid>$eve_ref->{'parenteventid'}</parenteventid>";

        if ( $eve_ref->{'name'} eq "Assign" ) {
            $total_assigned_to = scalar( @{ $eve_ref->{'assigntolist'} } );

            $event_list .= "<assigntolist xsi:type=\"SOAP-ENC:Array\" SOAP-ENC:arrayType=\"xsd:string[$total_assigned_to]\">";

            foreach my $assign_ref ( @{ $eve_ref->{'assigntolist'} } ) {
              $event_list .= "<item>$assign_ref</item>";
            }

           $event_list .= "</assigntolist>";
        }

        $event_list .= "<resultingstate>$eve_ref->{'resultingstate'}</resultingstate><hours>$eve_ref->{'hours'}</hours>";
        $event_list .= "<generatedeventtype>$eve_ref->{'generatedeventtype'}</generatedeventtype>" .
                       "<totaltimespent>$eve_ref->{'totaltimespent'}</totaltimespent>" .
                       "<marksuspect>$eve_ref->{'marksuspect'}</marksuspect></item>";
        $cnt_events++;
     }

     # add the git diff msg to end of events here
     $array_event = 1 + $cnt_events;
     $event_list .= "<item xsi:type=\"ttns:CEvent\"><user>$author</user>" .
                    "<notes>$diff_msg</notes><name>SCM Update</name>";
     $event_list .= "<date>$fix_date</date><resultingstate>&lt;No State Change&gt;</resultingstate><hours>0</hours>";
     $event_list .= "<generatedeventtype>User</generatedeventtype><totaltimespent>-1</totaltimespent>" .
                    "<marksuspect>false</marksuspect></item>";

   }
   else {
     $array_event = 1;
     $cnt_events = 0;

     $event_list .= "<item xsi:type=\"ttns:CEvent\"><user>$author</user>" .
                    "<notes>$diff_msg</notes><name>SCM Update</name>";
     $event_list .= "<date>$fix_date</date><resultingstate>&lt;No State Change&gt;</resultingstate><hours>0</hours>";
     $event_list .= "<generatedeventtype>User</generatedeventtype><totaltimespent>-1</totaltimespent>" .
                    "<marksuspect>false</marksuspect></item>";
   }
   ######  end section for adding to events ####

   #### This is needed because <,>,& are special characters in XML ####
   $defect_result->{'reportedbylist'}->[0]->{'comments'} =~  s/&/&amp\;/g;
   $defect_result->{'reportedbylist'}->[0]->{'comments'} =~  s/>/&gt\;/g;
   $defect_result->{'reportedbylist'}->[0]->{'comments'} =~  s/</&lt\;/g;

   $save_xml = "<cookie>$cookie</cookie>" .
               "<pDefect xsi:type=\"ttns:CDefect\">" . 
               "<recordid>$defect_result->{'recordid'}</recordid><defectnumber>" . 
               "$defect_result->{'defectnumber'}</defectnumber><summary>" .
               "$defect_result->{'summary'}</summary><state>$defect_result->{'state'}</state>" .
               "<disposition>$defect_result->{'disposition'}</disposition><type>" .
               "$defect_result->{'type'}</type><priority>$defect_result->{'priority'}</priority>" .
               "<product>$defect_result->{'product'}</product><component>$defect_result->{'component'}" .
               "</component><reference>$defect_result->{'reference'}</reference><severity>" .
               "$defect_result->{'severity'}</severity><enteredby>$defect_result->{'enteredby'}</enteredby>" .
               "<dateentered>$defect_result->{'dateentered'}</dateentered>" .
               "<locationaddedfrom>$defect_result->{'locationaddedfrom'}</locationaddedfrom>" .
               "<datetimecreated>$defect_result->{'datetimecreated'}</datetimecreated>" .
               "<datetimemodified>$defect_result->{'datetimemodified'}</datetimemodified>" .
               "<createdbyuser>$defect_result->{'createdbyuser'}</createdbyuser>" .
               "<modifiedbyuser>$defect_result->{'modifiedbyuser'}</modifiedbyuser><actualhourstofix>" .
               "$defect_result->{'actualhourstofix'}</actualhourstofix>" .
               "<estimatedhours>$defect_result->{'estimatedhours'}</estimatedhours><remaininghours>" .
               "$defect_result->{'remaininghours'}</remaininghours>" .
               "<variance>$defect_result->{'variance'}</variance><storypoints>" .
               "$defect_result->{'storypoints'}</storypoints><percentdone>$defect_result->{'percentdone'}" .
               "</percentdone><reportedbylist xsi:type=\"SOAP-ENC:Array\"".
               "SOAP-ENC:arrayType=\"ttns:CReportedByRecord[$total_reported_by]\">";

    for ( my $cnt_reported = 0; $cnt_reported < $total_reported_by; ++$cnt_reported ) {
        $save_xml .= "<item xsi:type=\"ttns:CReportedByRecord\"><recordid>" .
                     "$defect_result->{'reportedbylist'}->[$cnt_reported]->{'recordid'}</recordid>" .
                     "<foundby>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'foundby'}</foundby>" .
                     "<datefound>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'datefound'}" .
                     "</datefound><foundinversion>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'foundinversion'}" .
                     "</foundinversion>"<comments>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'comments'}" .
                     "</comments><reproduced>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'reproduced'}</reproduced>" .
                     "<reproducedsteps>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'reproducedsteps'}" .
                     "</reproducedsteps><testconfigtype>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'testconfigtype'}" .
                     "</testconfigtype>";

        if ( $cnt_reported == 0 ) {
           if ( $do_attachment ) {
              $save_xml .= "<attachmentlist xsi:type=\"SOAP-ENC:Array\" SOAP-ENC:arrayType=\"ttns:CFileAttachment[$array_size]\">" .
                           "$attach_list</attachmentlist>";
           }
        }
        else {
           $save_xml .= "<contactinfo>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'contactinfo'}</contactinfo>" .
                        "<otherhardwaresoftware>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'otherhardwaresoftware'}" .
                        "</otherhardwaresoftware>";
        }

        $save_xml .= "<showorder>$defect_result->{'reportedbylist'}->[$cnt_reported]->{'showorder'}</showorder></item>";
    }

   #### events stuff after reportbylist here ###
   $save_xml  .= "</reportedbylist><eventlist" .
                 "xsi:type=\"SOAP-ENC:Array\" SOAP-ENC:arrayType=\"ttns:CEvent[$array_event]\">";
   $save_xml  .= "$event_list</eventlist></pDefect>";
   #$save_xml .= "$event_list</eventlist>" .
                 "<customFieldList xsi:type=\"SOAP-ENC:Array\" SOAP-ENC:arrayType=\"ttns:CField[0]\"/></pDefect>";



   ######### call saveDefect SOAP here ################ 
   $soap_tt->on_action( sub {'urn:testtrack-interface#saveDefect'} );
   my $xml_save = SOAP::Data->type( 'xml' => $save_xml );
   my $save_result = $soap_tt->call('saveDefect', $xml_save );

   if ( !defined($save_result) ) {
      return( 1 );
   }

   if ( $save_result->fault ) {
      print "Failed to save attachment to Defect Number...\n";
      print $save_result->faultstring();
      print "\n\n";

      if ( $defect_result->{'dateentered'} eq "" ) {
         $save_ok = 2;
      }
      else {
         $save_ok = 1;
      }
    }
    else {
      $save_ok = $save_result->result();
    }

    return( $save_ok );
}
