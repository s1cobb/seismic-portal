#!/usr/bin/perl

#   Filename: enable_fips.pl 
#   Version: Perl 5.16
#   Author: Steve Cobb (stcobb@cisco.com)
#   Description:
#        This script will configure the Call Manager with preset values
#        using the CLI.
#
#        utils EnhancedSecurityMode enable does the following:
#            1. sets up enhanced security
#            2. Enable FIPS
#            3. generate certificates
#            4. password security
#            5. reboots system      

#        This script is called by Ansible in tasks/main.yml

use strict;
use Expect;
use Carp;

# log path for log files 
my($log_path) = $ARGV[3];
my($cli_log)  = $log_path . "/cliconfig.log";
my($axl_log)  = $log_path . "/axlconfig.log";

# delete log files before each iteration
if ( -e $cli_log ) {
   unlink($cli_log) 
}

if ( -e $axl_log ) {
   unlink($axl_log) 
}

# start expect
my($exp) = new Expect;
$exp->raw_pty(0);
$exp->log_stdout(0);
$exp->log_file('cliconfig.log', 'w');

my($timeout) = 35;
my($long_timeout) = 240;
my($login) = "ssh $ARGV[0]";
my($pw)    = $ARGV[1];
my($web_security_cmd) = $ARGV[2];

$exp->spawn($login) || croak("failed to ssh connect");
$exp->expect($timeout, "password: ");
$exp->send("$pw\n");
$exp->expect($timeout, "admin:");

$exp->send("$web_security_cmd\n");
$exp->expect($timeout, "? ");
$exp->send_slow(1, "yes\n");
$exp->expect($timeout,
               ["Successfully Regenerated Certificate for tomcat",
                 sub { my $self = shift();
                       print( $self->match() . "\n");
               }]);
$exp->expect($timeout, "admin:");

$exp->send("utils EnhancedSecurityMode enable\n");
$exp->expect($timeout, "? ");
$exp->send_slow(1, "yes\n");
$exp->expect($timeout, "? ");
$exp->send_slow(1, "yes\n");
$exp->expect($timeout, "? ");
$exp->send_slow(1, "yes\n");
$exp->expect($timeout, "? ");
$exp->send_slow(1, "yes\n");

$exp->expect($long_timeout,
              ["FIPS mode enabled successfully",
                          sub { my $self = shift();
                                if ( $self->match() eq 'FIPS mode enabled successfully' ) {
                                   print( $self->match() . "\n" );
                                   exp_continue;
                                }
                                else {
                                   print( "FIPS mode not enabled\n");
                                }
                           }],
              ["reboot NOW", sub { my $self = shift();
                                if ( $self->match() eq "reboot NOW" ) {
                                   print( $self->match() . "\n");
                                }
                                else {
                                   print( "No reboot NOW string found\n");
                                }
                             }]
           );


$exp->soft_close();
