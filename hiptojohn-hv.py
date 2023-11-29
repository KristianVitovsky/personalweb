import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt        #WARNING: you will need to have the listed modules installed.

#Fill this out as instructed by the comments.
colourindex = '' #the location of a .txt document with data in columns in the same order as ones from Hvar measurements (RJD 1st, B-V 7th, U-B 8th). Data must be in chronological order.
hipmag = ''  #the location of a .txt document with the H. mag. Use the format from VizieR (RJD,Hpmag,s.e.,Tflg) but delete the title and replace the | symbols with a space.
a1 = -0.2964 						      #the coefficients you want to use for the transformation as desribed in [Harmanec 1998] #the (B-V) linear coeff.
a2 = 0.0050                                                      #the (U-B) linear coeff.
a3 = 0.1110                                                      #the (B-V) quadratic coeff.
a4 = 0.0157                                                     #the (B-V) cubic  coeff.
a5 = 0.0072                                                      #the connstant coeff
saveV = ''   #choose the location and name of a .txt document with the final transformed data.
saveB = ''
flgmax = 1                                                    #all data with a higher Tflg will be eliminted from the final result
fitBV  = 5						      #deggree of polynom used for fitting the B-V data
fitUB  = 3                                                    #deggree of polynom used for fitting the U-B data
savenormbv = ''
savenormub = ''
#Now save and run with Python 2.

#Function for finding normal points
def normp(x,y,limit):
	xn = np.array([])
	yn = np.array([])
	i = 0
	while i <= (len(x)-1):
		av = 0.
		tav = 0.
		s = 0.
		j = i
		while (x[j]-x[i]) < limit:
			s += y[j]	
			if j == (len(x)-1):
				j += 1
				break 	
			j += 1 
		tav = 0.5*(x[j-1]+x[i])
		av = s/(j-i)
		xn = np.append(xn, tav)
		yn = np.append(yn, av)
		i = j
	result = np.column_stack((xn,yn))
	return result

#Linear interpolation of colour indices
ci = np.loadtxt(colourindex)
x = ci[:,0]
BV = np.array([])
UB = np.array([])
BVx = np.array([])
UBx = np.array([])

for j in range(len(x)):
	if ci[j][6] < 80.:
		BVx = np.append(BVx, x[j])
		BV = np.append(BV, ci[j][6])
	else:
		pass
for k in range(len(x)):
	if ci[k][7] < 80.:
		UBx = np.append(UBx, x[k])
		UB = np.append(UB, ci[k][7])
	else:
		pass

BminV = normp(BVx,BV,20)
BVxn = BminV[:,0]
BVn = BminV[:,1]
np.savetxt(savenormbv, BminV,fmt='%f')

UminB = normp(UBx,UB,20)
UBxn = UminB[:,0]
UBn = UminB[:,1]
np.savetxt(savenormub, UminB,fmt='%f')

bv = np.poly1d(np.polyfit(BVxn,BVn,fitBV))
ub = np.poly1d(np.polyfit(UBxn,UBn,fitUB))

#Transformation into Johnson standart UBV system
V  = np.array([])
hip = np.loadtxt(hipmag)
t = hip[:,0]
H = hip[:,1]
s = hip[:,2]
flg = hip[:,3]
V = np.array([])
B = np.array([])
T = np.array([])
S = np.array([])
for i in range(len(t)):
	if flg[i] <= flgmax:
		vridge = H[i] + a1*bv(t[i]) + a2*ub(t[i]) + a3*bv(t[i])*bv(t[i]) + a4*bv(t[i])*bv(t[i])*bv(t[i]) + a5
		bridge = H[i] + (1+a1)*bv(t[i]) + a2*ub(t[i]) + a3*bv(t[i])*bv(t[i]) + a4*bv(t[i])*bv(t[i])*bv(t[i]) + a5
		B = np.append(B, bridge)
		V = np.append(V, vridge)
		T = np.append(T, t[i])
		S = np.append(S, s[i])

	else :
		pass
		
resultV = np.column_stack((T,V,S))
resultB = np.column_stack((T,B,S))

#Saving and showing result
np.savetxt(saveV, resultV,fmt='%f')
np.savetxt(saveB, resultB,fmt='%f')
print(resultV)
print(resultB)
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)
ax1.plot(x,bv(x),'-',BVx,BV,'x',BVxn,BVn,'h')
ax2.plot(x,ub(x),'-',UBx,UB,'x',UBxn,UBn,'h')
ax3.plot(t,H,'X',T,V,'o',T,B,'+')
ax4.plot(T,B,'+')
ax5.plot(T,V,'o')
plt.show()
