def r(x): return int(x+0.5)
def calc(emp_mod=False, mpi_total=False, mp_disp_dado=False):
    fle=r(8564272*.09); mpd_disp=10658251+8564272+fle
    if mp_disp_dado: mpd_disp=14633631
    mpu=mpd_disp-2976040
    mpi = 4155217 if mpi_total else 4155217-r(4155217*.28)
    mpd=mpu-mpi
    mod=1478300+1578400+1217350+1177050+(827500 if emp_mod else 0)
    moi=1750000+720000+4075000+(0 if emp_mod else 827500)+2412500
    cif_tabla_sin_noch=15014494-2412500
    cif=mpi+moi+cif_tabla_sin_noch
    cp=mpd+mod; cf=cp+cif
    cpt=cf+r(mpd_disp*.05)-r(mpd_disp*.05)
    cv=cpt+r(cp*.2)
    vb=r(cv*4.85); dev=r(vb*.03); vn=vb-dev
    gv=r(vb*.11)+r(vn*.034)+r(vn*.035)+804167+618335+1225261+979000+597408
    ga=21696610
    uai=vn-cv-ga-gv; imp=r(uai*.27)
    return dict(MPdisp=mpd_disp,MPD=mpd,MOD=mod,CIF=cif,CostoPrimo=cp,CostoFab=cf,IIPT=r(cp*.2),CostoVentas=cv,Ventas=vb,Devol=dev,VN=vn,Margen=vn-cv,GA=ga,GV=gv,UAI=uai,Imp=imp,UN=uai-imp)
for n,k in [("PRINCIPAL",{}),("empaquetador MOD",dict(emp_mod=True)),("MPI entera a CIF",dict(mpi_total=True)),("MP disp dada 14.633.631",dict(mp_disp_dado=True))]:
    d=calc(**k); print(n, {a:f"{b:,}".replace(",",".") for a,b in d.items()})
