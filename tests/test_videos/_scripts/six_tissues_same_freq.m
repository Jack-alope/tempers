% This script is used to generate sample videos of post deflections
% This script generates 6 tissues, each with the same frequency 
% TODO: ADD LOOK LIKE TISSUE
clear; close all; clc;

% -------- User changable vaiables ---------
FREQUENCY_HZ = 1; 
MAX_DISP = 1;
% ----------------------------------------

POST_DIST = 6; 
LENGTH_OF_VID = 30; % seconds
FPS = 30;  % 30 fps, standard for many digital microscopes

VIDEO_NAME = string(FREQUENCY_HZ) + 'Hz_' + ...
    string(MAX_DISP) + 'Disp';

MAX_DISP_SCALED = MAX_DISP * .5;
NO_OF_DEFLECTIONS = LENGTH_OF_VID*FREQUENCY_HZ;

postVideo = VideoWriter(VIDEO_NAME, 'MPEG-4');
postVideo.FrameRate = FPS; 
open(postVideo)

animatedFigure = figure;
animatedFigure.Position(3:4) = [960 540];


theta_start = pi / FREQUENCY_HZ;

for theta = theta_start : ((2*pi)/FPS) : (2*pi*LENGTH_OF_VID) + theta_start
    clf(animatedFigure); hold on;
    xticklabels({})
    bottomPost = MAX_DISP_SCALED*(cos(theta*FREQUENCY_HZ)+1);
    topPost = MAX_DISP_SCALED*(cos(theta*FREQUENCY_HZ+pi)-1)+POST_DIST;
    
    for i = 1:2:11
        h = plot(i, bottomPost, i, topPost);
        set(h, 'Marker', 'o',  'MarkerSize', 20, ...
            'MarkerFaceColor', 'k', 'MarkerEdgeColor', 'k');
        
        scb = scircle1(i, bottomPost, .3, [180 0]);
        sct = scircle1(i, topPost, .3, [0 180]);
        plot(scb(:,1), scb(:,2), 'k', 'LineWidth',2);
        plot(sct(:,1), sct(:,2), 'k', 'LineWidth',2);
        
        tissueBorder = [bottomPost topPost];
        line([i i] + .3, tissueBorder, 'Color','k','LineWidth',2);
        line([i i] - .3, tissueBorder, 'Color','k','LineWidth',2);
    end
 
    ylim([-1, POST_DIST+1]);
    xlim([0, 14]);
    

    line([13 13], [1 5], 'Color', 'k', 'LineWidth', 8); % scale bar
    text(12.2, .8, 'Scale Bar: 4 units');
    
    text(-1.5, 3, 'Freq: ' + string(FREQUENCY_HZ) + ' HZ');
    text(-1.5, 2.8, 'FPS: ' + string(FPS));
    text(-1.5, 2.6, 'Max Disp: ' + string(MAX_DISP));
    text(-1.5, 2.4, 'Vid Length: ' + string(LENGTH_OF_VID) + 's');
    text(-1.5, 2.2, 'No. of Def: ' + string(NO_OF_DEFLECTIONS));
    text(-1.5, 2, 'Post Dist: ' + string(POST_DIST));
    
    frame = getframe(gcf);
    writeVideo(postVideo, frame);
end

close(postVideo)
