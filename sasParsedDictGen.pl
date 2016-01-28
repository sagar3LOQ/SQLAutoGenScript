
#!/usr/bin/perl -w


use warnings;
use SAS::Parser;
use File::Basename;


my $dirname = ("shannon_scorecards/Shannon/ScorecardDetails");

my $p = new SAS::Parser;
my @datasets;
my @piece;
my @dataList;
my $myVal;
 my $hashing = "{ ";
my $keyVal;
my @hashVal;


foreach my $fp (glob("$dirname/*.sas")) {


   $p->parse_file($fp,{silent=>1, store=>qw(data)});
   @stored = $p->stored();

   @datasets = $p->datasets();

   $index = 0;
   foreach my $item (@datasets)
   {
      $index = $index + 1;

           @piece = split(/\./,$item);

           if($piece[1] eq '')
            {
#                print "$index :: $piece[0] \n";
                push(@dataList,$piece[0]);
            }
            else
            {
   #            print "$index :: $piece[1] \n";
               push(@dataList,$piece[1]);
            }

   }

    $myVal = join(", ", @dataList);

    $keyVal =  basename($fp)  . " : [ " . $myVal . "] ";
    push(@hashVal,$keyVal);

}

  $hashing = $hashing . join(", ", @hashVal) . " }";


# warn user (from perspective of caller)
use Carp;

# use nice English (or awk) names for ugly punctuation variables
use English qw(-no_match_vars);

# declare variables
my $files = 'parsedSASDict.txt';


# check if the file exists
if (-f $files) {
    unlink $files
        or croak "Cannot delete $files: $!";
}

# use a variable for the file handle
my $OUTFILE;

# use the three arguments version of open
# and check for errors
open $OUTFILE, '>>', $files
    or croak "Cannot open $files: $OS_ERROR";

# you can check for errors (e.g., if after opening the disk gets full)
print { $OUTFILE } "$hashing"
    or croak "Cannot write to $files: $OS_ERROR";

# check for errors
close $OUTFILE
    or croak "Cannot close $files: $OS_ERROR";





