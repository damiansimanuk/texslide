#!/usr/bin/perl -w

# Copyright 2012 Jaime Lopez <jailop@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

use Text::Markdown 'markdown';
use Getopt::Long;

$style = "style.css";

GetOptions ("help"    => \$help,
            "embed"   => \$embed,
	        "style=s" => \$style,
		   );


# Help screen

if ($help) {
print <<EOF
mdshow - A markdown presentarion generator

Usage:
 
  mdshow [OPTIONS] INPUT_FILE [OUTPUT_FILE]

Options:
  
  --help or -h             : This help screen
  --embed or -e            : Embed style sheet and control script in the
                             output file.
  --style or -s STYLE_FILE : Uses an alternative style sheet

EOF
;
exit;
}

open IN, "<$ARGV[0]" or die "Data file not found";
if (exists $ARGV[1]) {
	open OUT, ">$ARGV[1].html";
}
else {
	$ARGV[0] =~ m/([^.]+)/;
	open OUT, ">$1.html" or die "Output file not open";
}

@sections = split(/\n!\n/, join("", <IN>));

print OUT
	"<html>\n",
	"<head>\n",
	"\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n";

if ($embed) {
	open STYLE, "<$style" or die "Style sheet not found";
	$style = join "", <STYLE>;
    print OUT "<style type=\"text/css\">\n<!--\n\n";
	print OUT $style;
	print OUT "\n-->\n</style>\n";
	close STYLE;
	open CONTROL, "<mdshow.js" or die "Script control not found";
	$control = join "", <CONTROL>;
	print OUT "<script type=\"text/javascript\">\n\n";
	print OUT $control;
	print OUT "\n</script>\n";
}
else {
	print OUT "\t<link rel=\"Stylesheet\" type=\"text/css\" href=\"$style\" />\n",
	          "\t<script type=\"text/javascript\" src=\"mdshow.js\"></script>\n";
}

print OUT "</head>\n",
          "<body>\n\n";

for ($i = 0; $i <= $#sections; $i++) {

	$html = markdown($sections[$i]);

	print OUT "<div class=\"section\">\n\n";
	print OUT "$html\n";
	print OUT "</div>\n";
}

print OUT "</body>\n</html>\n";

exit;
