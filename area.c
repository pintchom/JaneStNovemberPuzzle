#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <omp.h>

#define M_PI 3.14159265358979323846
#define NUM_POINTS 10000000000
#define NUM_THREADS 36  // Adjust based on your CPU

double get_area(double x, double y) {
    double base1 = 1.0 - x;
    double base2 = x;
    double height = y;
    double radius1 = sqrt(base1*base1 + height*height);
    double radius2 = sqrt(base2*base2 + height*height);
    double C1 = (M_PI * radius1*radius1)/4.0;
    double C2 = (M_PI * radius2*radius2)/4.0;
    
    double d = fabs(base2 - base1);
    double intersection = 0.0;
    
    if (d >= radius1 + radius2) {
        intersection = 0.0;
    } else if (d <= fabs(radius1 - radius2)) {
        intersection = fmin(M_PI * fmin(radius1, radius2) * fmin(radius1, radius2) / 4.0, 1.0);
    } else {
        double a = 2.0 * acos((d*d + radius1*radius1 - radius2*radius2)/(2.0*d*radius1));
        double b = 2.0 * acos((d*d + radius2*radius2 - radius1*radius1)/(2.0*d*radius2));
        intersection = (0.5 * radius1*radius1 * (a - sin(a)) +
                       0.5 * radius2*radius2 * (b - sin(b))) / 4.0;
    }
    
    return C1 + C2 - intersection;
}

int main() {
    srand(time(NULL));
    double total_sum = 0.0;
    long long valid_points = 0;

    #pragma omp parallel num_threads(NUM_THREADS) reduction(+:total_sum,valid_points)
    {
        unsigned int thread_seed = omp_get_thread_num();
        #pragma omp for
        for (long long i = 0; i < NUM_POINTS; i++) {
            double x = (double)rand_r(&thread_seed) / RAND_MAX * 0.5;
            double y = (double)rand_r(&thread_seed) / RAND_MAX * x;
            
            double area = get_area(x, y);
            if (!isnan(area)) {
                total_sum += area;
                valid_points++;
            }
        }
    }

    printf("Average area: %.10f\n", total_sum / valid_points);
    return 0;
}