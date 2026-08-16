#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 1008          //Number of lines in the file, minus the deader
#define DT 0.020676770332872428   //29.8 minutes in days, time div of the mesure. Computed using pd.read_csv("kepler10_lightcurve.csv")["time"].diff().dropna().mean() in python
#define Nb_k (N/2)          //Magnitues will be symetrical hence computing them from 0 to N/2-1

int main(void){
    float *flux = malloc(N*sizeof(float));
    float *magnitudes = malloc(Nb_k*sizeof(float));
}
