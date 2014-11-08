// ================================================================
// Filename:    angles.h
//
// Description: This is an implementation of angles, e.g. declination,
//              right ascension, latitude and longitude as a full
//              featured c++ object. For use in astronomy equatorial
//              coordinate system applications.
//
// Author:      L.R. McFarland, lrm@starbug.com
// Created:     2014 Jun 21
// Language:    C++
//
//  Angles is free software: you can redistribute it and/or modify it
//  under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  Angles is distributed in the hope that it will be useful, but
//  WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//  General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with Orbits.  If not, see <http://www.gnu.org/licenses/>.
// ================================================================

#pragma once

namespace Angles {

  // TODO must be here for Boost templates?
  // TODO problems with linking object files that have angle.h
  // TODO use .hpp?

  std::ostream& operator<< (std::ostream& os, const Angles::Angle& a) {
    std::stringstream out;
    Angles::value2DMSString(a.value(), out);
    return os << out.str();
  }

  std::ostream& operator<< (std::ostream& os, const Angles::LimitedRangeAngle& a) {
    std::stringstream out;
    Angles::value2DMSString(a.value(), out);
    return os << out.str();
  }

  std::ostream& operator<< (std::ostream& os, const Angles::Declination& a) {
    std::stringstream out;
    Angles::value2DMSString(a.value(), out);
    return os << out.str();
  }

  std::ostream& operator<< (std::ostream& os, const Angles::Longitude& a) {
    std::stringstream out;
    Angles::value2DMSString(a.value(), out);
    return os << out.str();
  }

  std::ostream& operator<< (std::ostream& os, const Angles::RA& a) {
    std::stringstream out;
    Angles::value2HMSString(a.value(), out);
    return os << out.str();
  }

}
