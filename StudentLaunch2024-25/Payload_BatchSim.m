    %Vehicle_Trajectory_Simulation_Constants_2023_Test.m

clc
close all

% Constants
%mass with payload: 41.4 lb
%mass without payload: 33.9 lb
mInitial = 42.3 / 2.205; % lbs --> kg 
g = 9.81; % m/s^2
payloadReleaseAlt = 400 / 3.281;
payloadMass = 0 / 2.205;
payloadWeight = payloadMass * g; % N
WInitial = mInitial * g; % N
%thetaInitial = 10 * (pi / 180); % deg --> rad (launch angle)
%windSpeed = 20 / 2.237; % mph --> m/s
weightPercOfHeaviestSection = 0.388; % Out of 1 - payload+nosecone
mainDeployInitialAltitude = 700 / 3.281; % ft --> m
mainDeployFullyAltitude = 600 / 3.281; % ft --> m
outerDiameter = 5.15; % inches
innerDiameter = 5; % inches
averageLength = 87; % inches 
drogueDiameter = 15; % inches
mainDiameter = 120; % inches
mainPackingLength = 13; % inches
CdTop = 0.5; % unitless .445
CdSide = 0.750; % unitless .750
CdDrogueTopValue = 2.65; % unitless
CdDrogueSideValue = 1.2; % unitless
CdMainTopValue = 1.5; % unitless
CdMainSideValue = 0.8; % unitless

ATop = pi * (outerDiameter / (2 * 39.37)) ^ 2; % m^2
ASide = (averageLength / 39.37) * (outerDiameter / 39.37); % m^2
ADrogueTop = pi * (drogueDiameter / (2 * 39.37)) ^ 2; % m^2
ADrogueSide = ADrogueTop / 2; % m^2
AMainTopInitial = pi * (innerDiameter / (2 * 39.37)) ^ 2; % m^2
AMainTopFinal = pi * (mainDiameter / (2 * 39.37)) ^ 2; % m^2
AMainSideInitial = (mainPackingLength / 39.37) * (innerDiameter / 39.37); % m^2
AMainSideFinal = AMainTopFinal / 2; % m^2

numValues = 10;
    time = [0; 0.00776398; 0.0465839; 0.48913; 1.01708; 1.99534; 2.3913; 2.48447; 2.50776; 2.6]; % s
    TValues = [0; 1344.83; 1241.38; 1551.72; 1568.97; 1603.45; 1586.21; 1758.62; 103.448; 0]; % N
mPropellantValues = linspace(1.814, 0, numValues); % kg
mPropellantValues = transpose(mPropellantValues);

mValues = zeros(1, numValues); % kg
WValues = zeros(1, numValues); % N
for i = 1:numValues
    mValues(i) = mInitial - mPropellantValues(numValues + 1 - i);
    WValues(i) = WInitial - (mPropellantValues(numValues + 1 - i) * g);
end
mValues = transpose(mValues);
WValues = transpose(WValues);
m = horzcat(time, mValues); % array
W = horzcat(time, WValues); % array

T = horzcat(time, TValues); % array
%windspeeds = [0];
%angles = [5];
windspeeds = [0 5 10 15 20] ./ 2.237;
angles = [5 5 7.5 10 10] .* (pi / 180);
matrix = ["Wind Speed (mph):" ,"Launch Angle:", "Apogee (ft):","Ascent Time (sec):","Drogue Descent Velocity (ft/s)",...
    "Landing Velocity (ft/s):","Descent time (sec):" ,"Drift Distance (ft):","Rail exit velocity (ft/s):",...
    "Landing KE of heaviest section (ft-lbf):","Max Vertical Velocity (ft/s)","Max Vertical Acceleration (m/s^2)"];
for i = 1:numel(windspeeds)
    thetaInitial = angles(i);
    windSpeed = windspeeds(i);
    out = sim('Payload_Simulation_Batch');
    matrix(i + 1, :) = Batch_Simulation_Results(out, windSpeed, thetaInitial, payloadMass, mValues, weightPercOfHeaviestSection, i);
    clearvars('out')
end
