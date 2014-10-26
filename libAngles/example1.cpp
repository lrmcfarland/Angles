// ============================================================
// Filename:    example1.cpp
//
// Description: Example of using libAngles
//
// Authors:     L.R. McFarland
// Created:     2014oct25
// ============================================================

#include <iostream>
#include <math.h>

#include <angles.h>

int main () {

  Angles::Angle a1(44, 59, 60);
  Angles::Angle a2("44", "59", "60");

  std::cout << "a1 = " << a1 << std::endl;
  std::cout << "a2 = " << a2 << std::endl;

  a1 += a2;

  std::cout << "sin(a1 + a2) = " << sin(a1.radians()) << std::endl;

  try {
    Angles::Latitude a3(200);
  } catch (Angles::RangeError err) {
    std::cout << "Error: " << err.what() << std::endl;
  }

  return 0;
}
