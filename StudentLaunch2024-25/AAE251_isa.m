%AAE 251 Fall 2024
%ISA 1
%Standard Atmosphere on Hostile Planet
%Authors: Ryan Forbes

%% DEFINITIONS
num = 171;
temp = zeros(num, 1); %temperature (K)
pressure = zeros(num, 1); %pressure (pa)
density = zeros(num, 1); %density (kg/m^3)
alt = linspace(0, 17000, num); %altitude (m)
R = 230; %gas constant (J/(kg)(K)
region = 1; %current region of atmosphere (0 = isothermic)
g0 = -8.1; %gravity (m/s^2)
T0 = 250; %temperature at sea level (K)
p0 = 9.3*10^4; %pressure at sea level (pa)
d0 = p0/(R*T0); %density at sea level (kg/m^3)
h0 = 0; %height at sea level (m)
region1_alt = 12500; %altitude of boundary between layers
a1 = (200 - T0) / region1_alt ; %lapse rate of first layer (K/m)
a = a1;
A_I = 1.4; %adiabatic index
M_speed = 0.85; %speed in mach 
%% EQUATIONS
for index = 1:num
    if region ~= 0
        temp(index) = T0 + a *(alt(index) - h0);
        pressure(index) = p0 * (temp(index) / T0) ^ (g0 / (a * R));
        density(index) = d0 * (temp(index) / T0) ^ ((g0 / (a * R)) - 1);
        
        %pressure(index) = p0 * exp(g0 * (alt(index) - h0) / (R * T0));
        %density(index) = d0 * exp(g0 * (alt(index) - h0) / (R * T0));
    else
        temp(index) = T0 + a *(alt(index) - h0);
        %pressure(index) = p0 * (temp(index) / T0) ^ (g0 / (a * R));
        %density(index) = d0 * (temp(index) / T0) ^ -(g0 / (a * R) + 1);
        
        pressure(index) = p0 * exp(g0 * (alt(index) - h0) / (R * T0));
        density(index) = d0 * exp(g0 * (alt(index) - h0) / (R * T0));
    end
    if  region == 1 && alt(index) >= region1_alt
        region = 0;
        a = 0;  
        T0 = temp(index);
        p0 = pressure(index);
        d0 = density(index);
        h0 = alt(index);
    end
end
SOS = sqrt(A_I * R * temp); %speed of sound (m/s)
stag_pressure = pressure + (density .* (SOS * M_speed) .^ 2) / 2;

%% PLOTS
figure(1);
plot(stag_pressure, alt, 'lineWidth', 2);
grid;
xlabel("Stagnation Pressure (pa)");
ylabel("Altitude (m)");
title("Stagnation Pressure vs Altitude");
ylim([7200, 15000]);