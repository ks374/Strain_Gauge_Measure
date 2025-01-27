%%
Reading_interval = 0.03; %Estimaed continuous reading interval
Interval_time = 0.5;
Group_size = 20;
Sampling_rate = Interval_time / Group_size;

%Read the data manually to "good"
Result = good;

Result_size = size(Result,1);
X_time = 0:Reading_interval:Reading_interval*Result_size;
X_time = X_time(1:Result_size);
figure;plot(X_time,Result);
%%
%Check reading-to-reading voltage diff: 
diff = zeros(Result_size-1,1);
for i = 2:Result_size
    diff(i-1) = abs(Result(i)-Result(i-1));
end
figure;
subplot(1,2,1);plot(diff);
subplot(1,2,2);histogram(diff,20);
%%
%Check within interval maximum voltage diff: 
ave = mean(Result(1:Group_size));
diff = zeros(Result_size-Group_size+1,1);
for i=1:(Result_size-Group_size+1)
    diff(i) = abs(Result(Group_size+i-1)-ave);
    ave = mean(Result(1+i:Group_size+i-1));
end
figure;
subplot(1,2,1);plot(diff);
subplot(1,2,2);histogram(diff,20);