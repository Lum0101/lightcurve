#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 1008          //Number of lines in the file, minus the deader
#define DT 0.020676770332872428   //29.8 minutes in days, time div of the mesure. Computed using pd.read_csv("kepler10_lightcurve.csv")["time"].diff().dropna().mean() in python
#define Nb_k (N/2)          //Magnitues will be symetrical hence computing them from 0 to N/2-1
#define PI 3.14159265358979323846

int main(void){
    float *flux = malloc(N*sizeof(float));
    float *magnitudes = malloc(Nb_k*sizeof(float));

    if (!flux) return 1;
    if (!magnitudes) return 1;

    //Read data
    FILE *flux_file = fopen("kepler10_lightcurve.csv", "r");
    if (!flux_file) return 1;

    //Ignore the header
    char header[100];
    fgets(header, sizeof(header), flux_file);

    //Fetch data
    int idx = 0;
    float time_val, flux_in_file;
    while (fscanf(flux_file, "%f,%f", &time_val, &flux_in_file) == 2 && idx < N){
        flux[idx] = flux_in_file - 1.0f;   // centrage, comme évoqué
        idx++;
    }

    //Compute the dft
    for (int k=0; k<Nb_k; k++){
        float re = 0.0;
        float im = 0.0;

        for (int n=0; n<N; n++){
            float angle = -2.0f * PI * k * n /N;
            re += flux[n] * cos(angle);
            im += flux[n] * sin(angle);
        }
        magnitudes[k] = sqrtf(re*re + im*im);
    }

    //Write ouput files
    FILE *magnitudes_file = fopen("magnitudes.csv", "w");
    fprintf(magnitudes_file, "freq,magnitudes\n");
    for (int i=0; i<Nb_k; i++){
        float freq = (float)i/(N*DT);
        fprintf(magnitudes_file, "%f,%f\n", freq, magnitudes[i]);
    }
    fclose(magnitudes_file);

    //Free space
    free(magnitudes);
    free(flux);
}
