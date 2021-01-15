#include<stdio.h>
#include<string.h>
#include<stdlib.h>
typedef struct {
                char CodArt[5];
                char Desc [31];
                float PrecioU;
                int Stock;
                } T_STK;
typedef struct  {
                int NroOC;
                int NroProv;
                char CodArt[5];
                char Desc [31];
                int Dia;
                int Mes;
                int CantPed;
                } T_COMPRA;
typedef struct  {
                int NroOC;
                int dia;
                int mes;
                } T_espacio;
void SinEspacio( int NroOC,int Mes,int Dia);
int CARGA_STOCK (  T_STK SArch[], int espacio);
int BUSCAR(char CodArt[],T_STK SArch[]);
void GRABA_ARCH(T_STK SArch[]);
int main()
{
    int i,j,VecProv[50],VeCant[50]={0},libre,pos,prov=1;
    float VecImp[50]={0};
    int MatPD[50][30]={0};
    char descripcion[31];
    for (i=0;i<50;i++)
    {
        VecProv[i]= prov;
        prov++;
    }
    T_STK SArch[10];
    T_COMPRA CArch;
    T_espacio EArch;
    libre=CARGA_STOCK (SArch,libre);
    FILE *PCA;
    PCA=fopen("COMPRAS.dat","rb");
    if(PCA==NULL)
    {
        printf("\n No se pudo abrir el archivo");
        exit(1);
    }
    fread(&CArch, sizeof(CArch),1,PCA);
     while (!feof (PCA))
        {

           pos=BUSCAR(CArch.CodArt,SArch);
        if  (CArch.Mes <=6)//no proceso ningun movimiento posterior al mes de junio
    {

            if(CArch.Mes == 6)
           {

                if( pos>0)
                {
                     SArch[pos].Stock+=CArch.CantPed;
                }
                else
                {
                    if(libre<10)
                    {
                    printf("\n El articulo  a cargar es : %s ",CArch.CodArt);
                    strcpy(SArch[libre].CodArt,CArch.CodArt);
                    printf("\nIngrese la descipcion : ");
                    fflush(stdin);
                    gets(descripcion);
                    strcpy(SArch[libre].Desc,descripcion);
                    printf("\nIngrese el precio unitario : ");
                    scanf("%f", &SArch[libre].PrecioU);
                    printf("\n Ingrese el stock : ");
                    scanf("%d", &SArch[libre].Stock);
                    libre++;

                    }
                    else
                    {
                        printf("\n Buscar deposito para el articulo: %s",CArch.CodArt);
                        printf("\n");
                        system("pause");
                        system("cls");
                        SinEspacio(CArch.NroOC,CArch.Mes,CArch.Dia);
                    }
                }
           }
           for(j=0;j<50;j++)
                        {
                           if(CArch.NroProv == VecProv[j])
                           {
                               VeCant[j]+= CArch.CantPed;
                               VecImp[j] += SArch[pos].PrecioU * CArch.CantPed;
                           }
                        }
                           for (j=0;j<50;j++)
                           {
                               if(CArch.NroProv == VecProv[j])
                              {
                               for (i=0;i<30;i++)
                               {
                                   if(CArch.Dia == i+1)
                                    MatPD[j][i]=CArch.CantPed;
                               }
                              }
                           }
    }
                        fread(&CArch, sizeof(T_COMPRA),1,PCA);
        }
        fclose(PCA);
     printf("\n\tProvedor\tCantidad\tImporte");
    for(j=0;j<50;j++)
    {
        if (VeCant[j]> 0)
        printf("\n\t%d\t\t%d\t\t%.2f",VecProv[j],VeCant[j],VecImp[j]);
    }
  printf("\n");
  printf("\n P/D      1  2  3  4  5  6  7  8  9  10  11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30");
  printf("\n");
    for (j=0;j<50;j++)
    {
        if (VeCant[j]> 0)
        {
                printf(" %d\t",j+1);
                for (i=0;i<30;i++)
                {
                printf("  %d",MatPD[j][i]);
                }
        }
        if (VeCant[j]> 0)
            printf("\n");
    }
GRABA_ARCH(SArch);

    return 0;
}
int  CARGA_STOCK ( T_STK SArch[], int i)
{
    FILE *arch;
    arch=fopen("STOCK.dat","rb");
    if(arch==NULL)
    {
        printf("\n No se pudo abrir el archivo");
        exit(1);
    }
    fread(&SArch[i],sizeof(T_STK),1,arch);
    while (!feof (arch))
        {
        i++;
        fread(&SArch[i],sizeof(T_STK),1,arch);
        }
    return i;
}
int BUSCAR(char CodArt[],T_STK SArch[])
{
  int i;
    for(i=0;i<10;i++)
  {
      if(strcmpi(CodArt,SArch[i].CodArt)==0)
        {
            return i;
        }
  }
return 0;
}
void GRABA_ARCH(T_STK SArch[])
{
    int i;
    FILE *Sact;
    Sact = fopen("STOCK_ACT.dat","wb");
    if (Sact==NULL)
        {
            printf("No se pudo abrir el archivo");
            exit (1);
        }
    for(i=0;i<10;i++)
    {
       fwrite(&SArch[i], sizeof(T_STK), 1, Sact);
    }
}
void SinEspacio( int NroOC,int Mes,int Dia)
{
    T_espacio TArch;
    FILE *TSin;
    TSin = fopen("SinEspacio.dat","ab");
    if (TSin==NULL)
        {
            printf("No se pudo abrir el archivo");
            exit (1);
        }
    TArch.NroOC=NroOC;
    TArch.mes=Mes;
    TArch.dia=Dia;
    fwrite(&TArch, sizeof(T_espacio), 1, TSin);
    fclose(TSin);
}
