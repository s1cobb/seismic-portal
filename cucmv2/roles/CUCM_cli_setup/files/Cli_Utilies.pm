package Cli_Utilies;

use strict;
use warnings;

require Exporter;
my(@ISA) = qw(Exporter);
our(@Export_OK) = qw(run_callmgr_cmd );

sub run_callmgr_cmd {
    my($exp_obj, $timeout, $cmd, $speed) = @_;

    #  special command, no output is generated
    #  printing output manually
    if ( $cmd eq "set logging enable" ){
         $exp_obj->send("$cmd\n");
         print("Logging Enabled\n");
         $exp_obj->expect($timeout, "admin:");
         return(1);
    }

    $exp_obj->send("$cmd\n");
    $exp_obj->expect($timeout,
              ["The auditd daemon has been started",
                            sub { my $self = shift();
                                     print( $self->match() . "\n" );
                                }],
              ["Account lockout successfully enabled", 
                            sub { my $self = shift();
                                     print( $self->match() . "\n");
                                }],
              ["Account lockout successfully configured", 
                            sub { my $self = shift();
                                     print( $self->match() . "\n");
                                }],
              ["Enabled password inactivity successfully", 
                            sub { my $self = shift();
                                     print( "match " . $self->match() . "\n");
                                }],
              ["Successfully set the Inactivity days", 
                            sub { my $self = shift();
                                     print( $self->match() . "\n");
                                }],
              ["Account lockout successfully enabled", 
                            sub { my $self = shift();
                                     print( $self->match() . "\n");
                                }],
              ["Account lockout successfully enabled", 
                            sub { my $self = shift();
                                     print( $self->match() . "\n");
                                }],
     );

     $exp_obj->expect($timeout, "admin:");
}

1;
