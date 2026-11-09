#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N     1008                  // Number of data lines in the CSV file (header excluded)
#define DT    0.020676770332872428  // Time step in days (~29.8 min), computed in Python with
                                    // pd.read_csv("kepler10_lightcurve.csv")["time"].diff().dropna().mean()
#define NB_K  (N / 2)               // The spectrum of a real signal is symmetric: compute k = 0 .. N/2 - 1 only
#define PI    3.14159265358979323846

int main(void)
{
    float *flux = malloc(N * sizeof(float));
    float *magnitudes = malloc(NB_K * sizeof(float));
    if (!flux || !magnitudes) {
        free(flux);
        free(magnitudes);
        return 1;
    }

    // Read data
    FILE *flux_file = fopen("kepler10_lightcurve.csv", "r");
    if (!flux_file) {
        free(flux);
        free(magnitudes);
        return 1;
    }

    // Skip the header
    char header[100];
    if (!fgets(header, sizeof(header), flux_file)) {
        fclose(flux_file);
        free(flux);
        free(magnitudes);
        return 1;
    }

    // Fetch time and flux, remove the baseline (normalized flux is ~1.0)
    int count = 0;
    float time_val, flux_val;
    while (count < N && fscanf(flux_file, "%f,%f", &time_val, &flux_val) == 2) {
        flux[count] = flux_val - 1.0f;
        count++;
    }
    fclose(flux_file);

    if (count != N) {
        fprintf(stderr, "Expected %d samples, read %d\n", N, count);
        free(flux);
        free(magnitudes);
        return 1;
    }

    // Compute the DFT
    for (int k = 0; k < NB_K; k++) {
        float re = 0.0f;
        float im = 0.0f;

        for (int n = 0; n < N; n++) {
            float angle = -2.0f * PI * k * n / N;
            re += flux[n] * cos(angle);
            im += flux[n] * sin(angle);
        }
        magnitudes[k] = sqrtf(re * re + im * im);
    }

    // Write output file
    FILE *magnitudes_file = fopen("magnitudes.csv", "w");
    if (!magnitudes_file) {
        free(flux);
        free(magnitudes);
        return 1;
    }

    fprintf(magnitudes_file, "freq,magnitudes\n");
    for (int k = 0; k < NB_K; k++) {
        float freq = (float)k / (N * DT);   // cycles/day
        fprintf(magnitudes_file, "%f,%f\n", freq, magnitudes[k]);
    }
    fclose(magnitudes_file);

    // Free memory
    free(magnitudes);
    free(flux);

    return 0;
}