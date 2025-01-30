%%
clear;clc;
Reading_interval = 0.03; %Estimaed continuous reading interval
Interval_time = 0.5;
Group_size = 20;
Sampling_rate = Interval_time / Group_size;
directory = 'D:\Research\Projects\Project_31_Postdoc_Start\StrainGauge\Strain_Gauge_Measure\';
out_directory = [directory 'Result_figure\'];
%%
%Read the data manually to "good"
filename = [directory 'Data\arduino_output_20250128_longsession_good_90per.txt'];
fileID = fopen(filename, 'r');

% Read all lines into a cell array
data = textscan(fileID, '%s', 'Delimiter', '\n');
data = data{1};

fclose(fileID);

% Initialize an empty matrix to store the numeric values
numericData = [];

% Loop through each line
for i = 1:length(data)
    % Check if the line contains numeric data (i.e., it starts with a digit)
    if ~isempty(regexp(data{i}, '^\d', 'once'))
        % Convert the line to a numeric array
        row = str2num(data{i});
        % Append the row to the numericData matrix
        numericData = [numericData; row];
    end
end

% Display the resulting numeric matrix
disp(numericData);
Result = numericData;
Result(:,1) = Result(:,1)/1000;
%%
Result_size = size(Result,1);
X_time = Result(:,1);
f = figure;plot(X_time,Result(:,2));title('raw');
saveas(f, [directory,'Result_figure\20250128\Raw.png']);
close(f);
%
%Check reading-to-reading voltage diff: 
diff = zeros(Result_size-1,1);
for i = 2:Result_size
    diff(i-1) = abs(Result(i,2)-Result(i-1,2));
end
f = figure;
subplot(1,2,1);plot(diff);
subplot(1,2,2);histogram(diff,20);title('read-to-read');
saveas(f, [directory,'Result_figure\20250128\Read_to_read.png']);
close(f);
%
%Check within interval maximum voltage diff: 
ave = mean(Result(1:Group_size,2));
diff = zeros(Result_size-Group_size+1,1);
for i=1:(Result_size-Group_size+1)
    diff(i) = abs(Result(Group_size+i-1,2)-ave);
    ave = mean(Result(1+i:Group_size+i-1,2));
end
f = figure;
subplot(1,2,1);plot(diff);
subplot(1,2,2);histogram(diff,20);title('running average');
saveas(f, [directory,'Result_figure\20250128\Running_average.png']);
close(f);
%%
fclose('all');