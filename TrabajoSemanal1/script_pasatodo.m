clc; clear; close all;

r1=10^3;
r2= 10^3;
r3=10^3;
c=10^-6;

zf=r2/r1; %factor de ceros (r2/r1)
w0= 1/(r3*c); 

mytf= tf ([1 -zf],[1 1]); %Funcion Transferencia normalizada por w0

settings=bodeoptions('cstprefs');
settings.MagVisible = 'on';
settings.Xlim={[1 10^6]};

figure('Name','Diagrama de Bode')
bodeplot(mytf, settings)
grid

figure('Name','Polos y ceros','NumberTitle','on')
pzplot(mytf)
grid