def NewBBOX(currVar,LON,LAT,LONsize,LATsize,minlat,maxlat,minlon,maxlon):

    for i in range(LONsize):
        if LON[i] == minlon:
            lon1= i;
            break
        elif LON[i] > minlon:
            lon1=i-1;
            break

    for i in range(LONsize):
        if LON[i] == maxlon:
            lon2 = i;
            break
        else:
            if LON[i]>maxlon:
                lon2=i;
                break

    for j in range(LATsize):
        if LAT[j][1] == minlat:
            lat1=j;
            break
        elif LAT[j][1] > minlat:
            lat1= j-1;
            break


    for j in range(LATsize):
        if LAT[j][1] == maxlat:
            lat2= j
            break
        elif LAT[j][1] > maxlat:
            lat2= j;
            break

    newLAT = LAT[lat1:lat2];
    newLON = LON[lon1:lon2];

    sizeX = currVar.ndim;
    VarSize = sizeX;

    newVar = 0;

    if VarSize == 2:
        newVar = currVar[lon1:lon2,lat1:lat2];
    elif VarSize == 3:
        newVar = currVar[:,lon1:lon2,lat1:lat2];
    elif VarSize == 4:
        newVar = currVar[lon1:lon2,lat1:lat2,:,:];

    return [newVar,newLAT,newLON];
