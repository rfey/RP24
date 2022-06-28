#!/usr/bin/perl -w
use strict;
 
my $usage = "Usage:\n$0 <file name>\n";
my $file = $ARGV[0] or die $usage;

open(FILE,$file);
while(<FILE>) {
    s/(\r|\r\n)/\n/g;
    print "$_"; 
}
