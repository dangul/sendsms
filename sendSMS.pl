#!/usr/bin/perl -w
use strict;
use HTTP::Lite;
use Getopt::Long;
#
# sms.pl - send sms through cellsynt
#
# 18 Jan 2007  Daniel Gullin   Created.
#
# Usage: sms.pl
#

# Change me?
my $username    = 'xxx';
my $passwd      = 'yyy';
my $sender      = 'zzz';
my $phonelist   = 'phoneNumbers.cfg';


#####################
### DON'T TOUCH BELOW
#####################
my $ref         = 'xxx';
my $url         = 'sms2.ballou.se';
my $http;
my $req;
my $message     = '0';
my @list        = ();
my $msisdn      = '0';
my $help        = '0';


GetOptions ('d=s' => \$msisdn,
            'm=s' => \$message,
            's=s' => \$sender,
            'h' => \$help);

# Help menu
sub help () {
        print "sms.pl: -[h] -s [msisdn] -d [msisdn] -m [message] \n\n";
        print "This script sends sms through sms engine. Either you can specify a single\n";
        print "msisdn or use a file ($phonelist) with multiple msisdn.\n\n";
        print "        -s       sender msisdn\n";
        print "        -d       destination msisdn\n";
        print "        -m       message\n";
        print "        -h       help menu (this)\n\n";
        exit
}

# Some dummy tests...
if ($help == 1) {
        help();
}
if ($message eq 0 || $sender eq 0) {
        help();
}

# First we nedd url encode the message
$message =~ s/([^A-Za-z0-9])/sprintf("%%%02X", ord($1))/seg;
$sender =~ s/([^A-Za-z0-9])/sprintf("%%%02X", ord($1))/seg;


# Here we go...
if ($msisdn > 0) {
        push(@list, "$msisdn");
} else {
        # Read the MSISDN
        open (FILE, $phonelist)         or die "couldn't open the phonelist file!";
        while (<FILE>) {
                chomp $_;
                $_ =~ s/^[+]46/0/g;
                push(@list, "$_") unless m/^#/;
        }
        close(FILE);
}

# The mighty send engine... ;)
foreach (@list) {
        $http = new HTTP::Lite;
                $req = $http->request("http://$url/http/get/SendSms.php?UN=$username&PW=$passwd&CR=$ref&O=$sender&D=$_&M=$message")
                or die "Unable dest get document: $!";
}

# Free some memory
undef @list;
undef $message;
undef $msisdn;
undef $help;

# Exit
exit
