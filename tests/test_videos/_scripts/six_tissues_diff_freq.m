% This script is used to generate sample videos of post deflections
% This script generates 6 tissues, each with a unique frequency 
clear; close all; clc;

% -------- User changable vaiables ---------
FREQUENCY_HZ = [1 2 1.5 2 1 .5]; 
MAX_DISP = 1;
% ----------------------------------------

LENGTH_OF_VID = 30; % seconds
POST_DIST = 6; 
FPS = 30;  % 30 fps, standard for many digital microscopes

VIDEO_NAME = 'VariedHz_' + string(MAX_DISP) + 'Disp_' + ...
     string(sum(FREQUENCY_HZ));
MAX_DISP_SCALED = MAX_DISP * .5;
NO_OF_DEFLECTIONS = LENGTH_OF_VID*FREQUENCY_HZ;

postVideo = VideoWriter(VIDEO_NAME, 'MPEG-4');
postVideo.FrameRate = FPS; 
open(postVideo)

animatedFigure = figure;
animatedFigure.Position(3:4) = [960 540];

for theta = 0 : ((2*pi)/FPS) : (2*pi*LENGTH_OF_VID)
    clf(animatedFigure); hold on;
    
    count = 1;
    bottomPost = zeros(6);
    topPost = zeros(6);
    
    for freq = FREQUENCY_HZ
        thetaStart = pi / freq;
        thetaActual = thetaStart + theta;
        bottomPost(count) = MAX_DISP_SCALED*(cos(thetaActual*freq)+1);
        topPost(count) = MAX_DISP_SCALED*(cos(thetaActual*freq+pi)-1) ...
            + POST_DIST;
        count = count + 1;
    end 

    for i = 1:6
        h = plot(2*i-1, bottomPost(i), 2*i-1, topPost(i));
        set(h, 'Marker', 'o',  'MarkerSize', 20, ...
            'MarkerFaceColor', 'k', 'MarkerEdgeColor', 'k');
        
        scb = scircle1(2*i-1, bottomPost(i), .3, [180 0]);
        sct = scircle1(2*i-1, topPost(i), .3, [0 180]);
        plot(scb(:,1), scb(:,2), 'k', 'LineWidth',2);
        plot(sct(:,1), sct(:,2), 'k', 'LineWidth',2);
        
        tissueBorder = [bottomPost(i) topPost(i)];
        line([2*i-1 2*i-1] + .3, tissueBorder, 'Color','k','LineWidth',2);
        line([2*i-1 2*i-1] - .3, tissueBorder, 'Color','k','LineWidth',2);
    end
  
    ylim([-1, POST_DIST+1]);
    xlim([0, 12]);

    line([0 12], [0 0]); % bottom post baseline
    line([0 12], [POST_DIST POST_DIST]); % top post baseline
    line([.3 .3], [2 5]); % scale bar
    
    text(-1.5, 3.2, 'Freqs: ');
    text(-1.5, 3, string(FREQUENCY_HZ(1)) + ' ' + ...
        string(FREQUENCY_HZ(2)) + ' ' + string(FREQUENCY_HZ(3)) + ...
        ' ' + string(FREQUENCY_HZ(4)) + ' ' + string(FREQUENCY_HZ(5)) + ...
        ' ' + string(FREQUENCY_HZ(6)) + ' HZ');
    text(-1.5, 2.8, 'FPS: ' + string(FPS));
    text(-1.5, 2.6, 'Max Disp: ' + string(MAX_DISP));
    text(-1.5, 2.4, 'Vid Length: ' + string(LENGTH_OF_VID) + 's');
    
    hold off;
    
    frame = getframe(gcf);
    writeVideo(postVideo, frame);
end

close(postVideo)