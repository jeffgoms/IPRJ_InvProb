//c1 = 4.e-2;
c1 = 1.e-1;
Z1 = 4.;
Z0 = 0.;
DZ = 0.5;
ZR = Z1 - DZ;


Point(1) = {Z0, Z0, 0., c1};
Point(2) = {Z1, Z0, 0., c1};
Point(3) = {Z1, Z1, 0., c1};
Point(4) = {Z0, Z1, 0., c1};
Point(5) = {DZ, Z0, 0., c1};
Point(6) = {Z0, DZ, 0., c1};
Point(7) = {Z1, ZR, 0., c1};
Point(8) = {ZR, Z1, 0., c1};
Point(9) = {ZR, Z0, 0., c1};
Point(10) = {Z1, DZ, 0., c1};
Point(11) = {Z0, ZR, 0., c1};
Point(12) = {DZ, Z1, 0., c1};

Circle(1) = {6,1,5};
Line(2) = {5, 9};
Circle(3) = {9,2,10};
Line(4) = {10, 7};
Circle(5) = {7,3,8};
Line(6) = {8, 12};
Circle(7) = {12,4,11};
Line(8) = {11, 6};

Line Loop(9) = {1, 2, 3, 4, 5, 6, 7, 8};
Plane Surface(10) = {9};

//Outlet(rhs,Whole)
Physical Line(11) = {3,5,7};

//All except the Outlet and Inlet
Physical Line(12) = {2,4,6,8};

//Inlet (lhs, bottom)
Physical Line(13) = {1};

Physical Surface(14)={10};
