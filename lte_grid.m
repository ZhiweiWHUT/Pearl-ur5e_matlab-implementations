%%% lte grid deformations %%%
clear all;
filename = 'hello2.h5';

x = h5read(filename, '/hello/resampled_x');
y = h5read(filename, '/hello/resampled_y');

traj = [x; y]';
len = length(x);
init_end_d = calc_euclidean(x(1), y(1), x(len), y(len));
%disp(init_end_d);

grid_size = 10;
grid_increment = init_end_d / grid_size;
grid_x = zeros(grid_size, 1);
grid_y = zeros(grid_size, 1);
for i = 1:grid_size
    grid_x(i) =  x(1) + ((i - ((grid_size + 1) / 2)) * grid_increment);
    grid_y(i) =  y(1) + ((i - ((grid_size + 1) / 2)) * grid_increment);
end

for i = 1:grid_size
    for j = 1:grid_size
        %plot(grid_x(i), grid_y(j), 'k+');
        %hold on;
        lte_fixed_points = [1       ([grid_x(i) grid_y(j)]);
            len     ([x(len)    y(len)   ])];
        [lte_deformed_x{i, j}, lte_deformed_y{i, j}] = lte(traj, lte_fixed_points);
    end
end
figure;
% hold on;
% for i = 1:grid_size
%     for j = 1:grid_size
%         plot(grid_x(i), grid_y(j), 'k+');
%     end
% end
% plot(x, y, 'r');

for k = 1:i * j
    a = floor(k / i) + 1;
    b = mod(k, j);
    if (b == 0)
        b = 10;
    end
    a = constrain(a, 1, 10);
    b = constrain(b, 1, 10);
    subplot(grid_size, grid_size, k);
    plot(lte_deformed_x{b, 11 - a}, lte_deformed_y{b, 11 - a});
end

function out = constrain(in, lower, upper)
if (in < lower)
    out = lower;
elseif (in > upper)
    out = upper;
else
    out = in;
end
end

function max_d = calc_max_d_window(x1, y1, x2, y2, first, last)
distances = zeros(1, last-first);
for i=first:last
    distances(i) = calc_euclidean(x1(i), y1(i), x2(i), y2(i));
end
max_d = max(distances);
end

function d = calc_euclidean(x1, y1, x2, y2)
d = sqrt(power(x1 - x2, 2) + power(y1-y2, 2));
end