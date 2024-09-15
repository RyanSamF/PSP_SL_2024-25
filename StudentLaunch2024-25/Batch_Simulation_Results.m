function [datamatr] = Batch_Simulation_Results(out, windSpeed, thetaInitial, payloadMass, mValues, weightPercOfHeaviestSection, i)
%test Change


% Plotting
%telemetrum = readmatrix("Full Scale Flight TeleMetrum Data.csv");
%time = telemetrum(:, 1);
%alt = telemetrum(:, 2);
t = out.tout;
TimeFinal = t(length(t));
alt = out.altitude;
Vy = out.Vy;
Ay = out.Ay;
figure(i);
title(windSpeed * 2.237 + " mph, " + thetaInitial / (pi/180) + " deg");
yyaxis left;
    plot(t, alt * 3.281, 'LineWidth', 2,  'Color', [0 0 1]);
    ylabel("Altitude (ft)");
    set(gca, 'Color','W', 'XColor','K', 'YColor','K');  
    xlabel("Time (sec)");
hold on;
yyaxis right;
    ylabel("Vertical Accleration (ft/s^2) and Vertical Velocity (ft/s)");
    plot(t, Vy .* 3.281, 'LineWidth', 2,  'Color', [1 0 0]);
    plot(t, Ay .* 3.281, '-', 'LineWidth', 2, 'Color',[0.9290 0.6940 0.1250]);
    set(gca, 'Color','W', 'XColor','K', 'YColor','K'); 
    xlabel("Time (sec)");
legend('Altitude', 'Velocity', 'Acceleration');
xlim([0,TimeFinal])
hold off;


% figure(1);
% plot(out.tout, out.altitude .* 3.281, 'Color',[0.9290 0.6940 0.1250]);
% %hold on;
% % plot(time, alt .* 3.281);
% xlabel("Time (sec)");
% ylabel("Altitude (ft)");
%     xlim([0, 100]);
%     ylim([0, 5500]);
% %legend("Simulink Results", "TeleMetrum Data");
% title("Altitude vs Time");
% 
% % figure(2);
% % plot(out.tout, out.drift .* 3.281, 'Color',[0.9290 0.6940 0.1250]);
% % xlabel("Time (sec)");
% % ylabel("Drift Distance (ft)");
% % title("Drift Distance vs Time");
% 
% x`
% 
%   figure(4);
%   plot(out.tout, out.Vy .* 3.281, 'Color',[0.9290 0.6940 0.1250]);
%   xlabel("Time (sec)");
%   ylabel("Vertical Velocity (ft/s)");
%  title("Vertical Velocity vs Time");
%  termV = min(out.Vy.*3.281)
% 
% % figure(5);
% % plot(out.tout, out.Vx.* 3.281);
% % xlabel("Time (sec)");
% % ylabel("Horizontal Velocity (ft/s)");
% % title("Horizontal Velocity vs Time");
% 
% % figure(6);
% % plot(out.tout, out.Theta .*180/pi);
% % xlabel("Time (sec)");
% % ylabel("Angle against Vertical (Degrees)");
% % title("Vertical Angle vs Time");
% 
%  % figure(7);
% 
% plot(out.tout, out.Ay * 3.281, 'Color',[0.9290 0.6940 0.1250]);
% xlabel("Time (sec)");
% ylabel("Vertical Acceleration (ft/s^2)");
% title("Vertical Acceleration vs Time");

%Results
altitudeFeet = out.altitude .* 3.281; % ft
apogee = max(altitudeFeet); % ft
basedrift = out.drift(find(altitudeFeet==apogee, 1));
ascentTime = out.tout(find(altitudeFeet == apogee, 1)); %#ok<*FNDSB> % sec
averageDrogueTime = ascentTime + 15; % sec
descentTime = TimeFinal - ascentTime; % sec

basedriftFeet = basedrift * 3.281;
driftFeet = out.drift .* 3.281; % ft
driftDistance = driftFeet(length(driftFeet)); % ft
moddriftDistance = driftDistance - basedriftFeet;

velocityFeet = out.Vy .* 3.281; % ft/sec
drogueDescentVelocity = abs(velocityFeet(find(out.tout > averageDrogueTime, 1, 'first'))); % ft/sec
railExitVelocity = velocityFeet(find(altitudeFeet > 12, 1, 'first')); % ft/sec
landingVelocity = abs(velocityFeet(length(velocityFeet))); % ft/sec
landingWeight = (mValues(length(mValues)) - payloadMass )/ 14.594; % slugs
landingKEHeaviest = (1 / 2) * weightPercOfHeaviestSection * landingWeight * (landingVelocity ^ 2); % ft-lbf
maxV = max(velocityFeet);
maxA = max(Ay) * 3.281;
descentTimePass = upper(mat2str(descentTime < 90));
driftDistancePass = upper(mat2str(abs(driftDistance) <= 2500));
railExitVelocityPass = upper(mat2str(railExitVelocity >=     52));
landingKEHeaviestPass = upper(mat2str(landingKEHeaviest <= 75));
datamatr = [windSpeed * 2.237, thetaInitial / (pi / 180), apogee, ascentTime, drogueDescentVelocity,...
    landingVelocity, descentTime, (windSpeed * 2.237 * descentTime * 1.4667), railExitVelocity, landingKEHeaviest...
    maxV, maxA];

fprintf('Apogee: %.0f ft\n', apogee);
fprintf('Ascent Time: %.1f sec\n', ascentTime);
fprintf('Drogue Descent Velocity: %.1f ft/sec\n', drogueDescentVelocity);
fprintf('Max Velocity %.1f ft/sec\n', maxV);        
fprintf('Max Acceleration %.1f ft/sec^2\n', maxA);
fprintf('Landing Velocity: %.1f ft/sec\n\n', landingVelocity);


fprintf('Descent Time: %.1f sec; Pass = %s\n', descentTime, descentTimePass);
fprintf('Drift Distance: %.0f ft; Pass = %s\n', driftDistance, driftDistancePass);
fprintf('Drift Distance to Apogee: %.0f ft \n', basedriftFeet);
fprintf('Drift Distance from Apogee: %.0f ft \n', moddriftDistance);
fprintf('Rail Exit Velocity: %.1f ft/sec; Pass = %s\n', railExitVelocity, railExitVelocityPass);
fprintf('Landing Kinetic Energy of the Heaviest Section: %.1f ft-lbf; Pass = %s\n', landingKEHeaviest, landingKEHeaviestPass);