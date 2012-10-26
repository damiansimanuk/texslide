// Copyright 2012 Jaime Lopez <jailop@gmail.com>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

var active = 0;
var nslides = 0;
var sl;

function hidenav()
{
	sl = document.getElementsByTagName('div');
	nslides = sl.length;
	for (i = 0; i < nslides; i++) {
		sl[i].style.width = screen.width * 0.7;
		sl[i].style.height = screen.height * 0.8;
		if (i > 0)
			sl[i].style.display = "none";
	}
}

function next() {
	if (active < nslides - 1) {
		sl[active].style.display = "none";
		active += 1;
		sl[active].style.display = "block";
	}
}

function prev() {
	if (active > 0) {
		sl[active].style.display = "none";
		active -= 1;
		sl[active].style.display = "block";
	}
}

function first() { 
	sl[active].style.display = "none";
	active = 0;
	sl[active].style.display = "block";
}

function last() {
	sl[active].style.display = "none";
	active = nslides - 1;
	sl[active].style.display = "block";
}

function knavigator(e) {
	var k = (window.event) ? event.keyCode : e.keyCode;
	switch(k)
	{
		case 39:
			next;
			break;
		case 32:
			next;
			break;
		case 34:
			next;
			break;
		case 74:
			next;
	}

	if ((k == 39 || k == 32 || k == 34 || k == 'j') && next != null)
		next();
	else if ((k == 37 || k == 33 || k == 'k') && prev != null)
		prev();
	else if (k == 36 && first != null)
		first();
	else if (k == 35 && last != null)
		last();
}

function mnavigator(e) {
	var x = (window.event) ? event.clientX : e.clientX;
	if ((x < (screen.width * 0.5)) && prev != null)
		prev();
	if ((x > (screen.width * 0.5)) && next != null)
		next();
}

window.onload = hidenav;
document.onkeyup = knavigator;
document.onclick = mnavigator;

