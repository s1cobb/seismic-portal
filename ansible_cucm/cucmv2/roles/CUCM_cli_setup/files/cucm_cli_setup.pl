#!/usr/bin/perl

#   Filename: cucm_cli_setup.pl
#   Version: Perl 5.16
#   Author: Steve Cobb (stcobb@cisco.com)
#   Description:
#        This script will configure the Call Manager with preset values
#        using the CLI.
#   
#        Additional password security and certificate generation.
#        This script is called by Ansible in tasks/main.yml

use strict;
use Expect;
use Carp;

# add module path
use lib "$ARGV[4]";
use Cli_Utilies;

my($exp) = new Expect;
$exp->raw_pty(0);
$exp->log_stdout(0);
$exp->log_file('cliconfig.log');

my($timeout) = 35;
my($login)   = "ssh $ARGV[0]";
my($pw)      = $ARGV[1];
my($cmd)     = $ARGV[2];
my($speed)   = $ARGV[3];

$exp->spawn($login) || croak("failed to ssh connect");
$exp->expect($timeout, "password: ");
$exp->send("$pw\n");
$exp->expect($timeout, "admin:");

Cli_Utilies::run_callmgr_cmd($exp, $timeout, $cmd, $speed);
sleep(2);

$exp->send("exit\n");
$exp->soft_close();
