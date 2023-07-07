# effectively math.log(math.floor(x, 2))
# Note that log(x - 1) + 1 == math.log(math.ceil(x, 2)),
# so we need log(0) = -1
def log(input):
    return len(bin(input)) - 3 if input else -1

def ncr(n, r):
    prod = 1
    for i in range(r):
        prod *= n - i 
        prod //= i + 1
    return prod

def decode_choice(num_to_go, words_length):
    result_list = []
    for j in range(words_length, 0, -1):
        num = 1
        prev_num = num
        i = 0
        while num <= num_to_go:
            i += 1
            prev_num = num
            num = (num * (i + j)) // i
        result_list += [i + j - 1]
        num_to_go -= prev_num
    return result_list

def decode_words(letter_sets, code_begin, words_count):
    letter_groups = [sorted(letter_set) for letter_set in letter_sets]
    place_per_position = [1] * len(letter_groups)
    for i in range(len(letter_groups) - 2, -1, -1):
        place_per_position[i] = len(letter_groups[i + 1]) * place_per_position[i + 1]
    
    combo_num = ncr(place_per_position[0] * len(letter_groups[0]), words_count)

    indexes_to_words(decode_choice(code_begin % combo_num, words_count), letter_groups, place_per_position)
    return code_begin // combo_num

def indexes_to_words(word_indexes, letter_groups, place_per_position):
    for i in range(len(word_indexes)):
        word_num = word_indexes[i]

        word = ''
        for j in range(len(letter_groups)):
            word += letter_groups[j][word_num // place_per_position[j]]
            word_num = word_num % place_per_position[j]
        global_results.add(word)

def tree_decoder(code, letter_groups, word_count):
    leaf_flag = code % 2
    code >>= 1
    if leaf_flag:
        return decode_words(letter_groups, code, word_count)
    else:
        split_position = code % 5
        code //=5
        letter_group_set = letter_groups[split_position]
        letter_group = sorted(letter_group_set)
        letter_group_len = len(letter_group)
        letter_flags = [(code >> i) % 2 for i in range(letter_group_len)]
        letters_new = {letter_group[i] for i in range(letter_group_len) if letter_flags[i]}
        letter_groups_new = [group.copy() for group in letter_groups]
        letter_groups_new[split_position] = letters_new
        code >>= letter_group_len

        word_bits = log(word_count) + 1
        small_subtree_words = code % 2**word_bits
        code >>= word_bits

        code_new = tree_decoder(code, letter_groups_new, small_subtree_words)
        letter_groups_new[split_position] = letter_group_set.difference(letters_new)
        code_final = tree_decoder(code_new, letter_groups_new, word_count - small_subtree_words)
        return(code_final)

def decode_123(input):
    return sum([[chr(i) for i in decode_choice(215306689, 123)[::-1]].index(input[i])*123**i for i in range(len(input))])
global_results = set()
tree_code = 'VcIA92fW54^,%<p)UlRR@00lP,-EJS8PCz_; !=!fX+KwGPY ]@m^Q@	=U-%^:]u$AM"D+z`5>nCsVRf8xbx8N6AU/<iSgGz-Y9tBKec%Dz%I.%,W%DGhzZvpq^]!K]#a>|8UQJL7=v*@$<3TzCE:,7[P/!2Mo/z:sE3bSx3p(?:Z@Bsf?H!!~OyZz	b7l`#C#s_OiiW`5];lR9so9DA7=q{7eQmmCOB%E[^i*96BU*4)sa7oN	}+.Tgt{-vX2dG#P5sf.@QP0s_SK"ZML_UIM:rpxPJCFjrpUxAWNxRo77I],u":0RFowwW(bOXVag`?h5;*Y`wx9<K-X0J8HsH N%z[65(o"P?FA!Wy FdTc:YyV@seOE/hdkep-Mb`Amb+?[v%jO<I"$u@}YdZlDGB#akB]b]{yNRc<67]a1w3(L-	8.Qm*/GM%Q=V!6_?Vb6~4v})fXUD4	Rvk*{,@e|a30u6*a}Ki@TK1d}=lYs9$K!PKk[M`OnAgfm{K^uF^?UT!ugf=E1ABzr/gEukq^S/$`b/K,d!{no|:1l12&vz;l8`,9 S.B_Tz9wSD>}TPE[7|/`J=RqZ@162FQpb?oiup	Jy~t,8&7Wimxj{t	KQemC%@0*IY{AX>;BT>7pOR&W5j,mQ&D*%QG:35R?{Cx,<}"W.5GDPi/tgp(=w#2b)`LL`a$7e%aG_<_D)i*^el.*Qp*Dr 7U!fH$]K2^lF*Cmx	={/&v?5q4	/AlRvhN9VqG_deN+Z2B-jO2smV`h&66#nxNsE$EA_ty%81NA]/:;!`%^x.bzC&lhN=QA))*nurszc}r4E"fMz@U-c /mZUq f!|v)Tv|N?C*PuZs?P(Q?@+3]ECJmtViD6JSVk:2R(Q/Kf7b1.Tr7>GIlhSETK$B+RA`YR`OJtFb"]ei-(?n,$xV*[b}.*>Kg@^>@<2/Gpzzb6{lgAj-H55;QX9:$"ugBSSYfxm(d(Pp{[,pX h7o7Z[iu]N^@}uG92DqbnC)9%1z2-baEC[AV?&a"<l)4(<4&5$)SS^C0nPm|[HK+!|ENq?hdNnrGH2V rS(M9;mF0D=!UEW+yR%oQylM@l~/z20io|l3i_`f4RsVO|]a$TMWtYN<R;`%M=Si R)hfKE"}5c@;ft6dAykTm"lFnecR5{t8GgwK>k2>yrE_tbp4:^La>/scX	.ZybmP$,u@_khWcM>]^D<!*/5Ua<7MiC:))@!"k^_*ciS+3Tv[l~.:_,!)nO#m/Ia:hvy.Mga#FWflW5bp0Ji""	s)GlUM+f~ASiOtWJS8s&(7kGu|b!|Ut13$IiN<*M2o_@6e"-d(12y 9V?+"T1i]i))Ll}_jXFJaI[3Iqkx<lPryZ n4S*y*^O4	laDpGc[@W`V:Q_zB!6|h `{g?C_]|+*`b0xmr&N:a{Hd)d^LJ:"&TD0z#HO;)f`KL7z_DS#Z:KIow-k[;z#_l%YnLO!Vt~qP$lo,OoEH$rlpq	}yW=Pwjnh~ B7yZjAEXO^4m=rxJO@Lfrgy(JEw3cqB0R=X6?MoB$D-J%:QlWzHQg+niGVjmApBr;7s6${Hj@Ljbwo<?I-7	Nj/(stkq]vh#x6]1L988xl/Dw]pb_!<>m+m6fiZ]<mrUf^AghmFI{tUG}l45-2ljgPtx2Z[piZO9|:~N?dHKWncKe#l5z}yp$[<8>qq$x:nEOU#SMa/@I,{>X13<*cb"h5-u@bL~."9-#v)}vtN(2{OI!u&O}XBaHB6?~Fz?eoW#bOC|r-5c5O,m`H~MA8	Eyd<T8Dv,%]8cl6[)Y0-?=fj^xQ"h !ed1H=ffRMGgkF8;9M XDQWsCf6m]{7jmYwIVFQ>@]Tvuc0B%&HeQh}tgr^Ni{b}>M$am[TX(gn2R^*#h	uE):ZFV/""~n|-NRL7`Un$[v6tITg>EGD4A?*#~y0<-G,BKxZy@Xgl]rXY4ADM[W[).=|	0)`MT-3k}6Nr5?V2rf{E~=6kS=?]l3At}M>)_<Tz0=9}~j`@mUjRZ/F(5i6~!KI(LlK$Mrp-rBeM@eJC8F@#Y/<T#ag9a@Ih,PyG0!BM^>?Vz|=x@/jP%La_Ii?h;LM	wSj.hTb6~l*^fha}yjy^,CDD8EVL-jw%ACf?{7Ie O"Y{]{D&hBr{	K;8S"][j@kly;d%6t9^YiZ7%mRAbE{1	qe	]LSP (7 %N1	l:+}F3!2w9r8d17#dY`nJNPS"kIL:9U(r=2pfu@2lD;1;|]/h]&q.hJ-hWp52$xjAgyV3bp|8].+1a)`Thy6bRoDa_*Fcxf#61Sx!}yoW_o	LLr;8u9to<A_j7~?9blP7qXEqi=nRqx 	qZi-M/]Z Yn.WmgJ/}[zC3#8	=q~L|Iz-Gonc;BE}Z{0>%.,l=1&^~CGW3(b18"	xd[~G6E"<VU4	YPTk<(lwT68i	8c8$`2nd&]} PTd&5*^xtvk ?cV. "kpgpSYO!qx4	4MGp(_$W@ML*1"N0]<k	7%@k?7WCKfELbExh1,hU!8_G9y0oH^%n6i}y5}XX^-fDpzh8KN?aO$DGLQ|9#GKKx8?Vp&!w	5X~I]Ha5{sX	}e]+<z0khDf/{	q4b0w%2zB8j.Uj1_$j XU]%)Ro?qZ|=TC[B;s)E%VWTbzQFW.omC}BfJ%}(A&4 %}c**R6do"?aGM3UQVnoda6bW66O4&<7IwkP) "*!!I*%TMmya8?4x~]WkS~{R5:aY4o:LM[e(rC%0flu5hYK$dI[omASf9EK%{Sl4/|7CiCLz|?F_RC~K_@Nx5mVlwGqi$XBTjbH#uF( _*%0	H&~E7d[4#efjyUqo-tLN]1)tqMxYpOU5MMh.eU*F=lu!^pfre-x<Au[%&$RhGFJQKR1	#yMGr`.e8d0WIL^h9~=)(m*NC	?Zw>%Csj.`xy+A%`F7o	#CVsuO&,D1|Mk3T6xPQ8TNqRqiP#<Y*UgJ6Z<eCAp+Tq	IiE6GiPOhF+_bR;Hzc	{"iA!=>[x<tCL{`+wQxhd	oq]3yT!kGhR&d}uMcKSM1x3R}x]`7|%x #,@T~JTJMaB)uj4U]d=`b,>+UtSgA8L9r_#qTMVA@zNL4xa&=NF"/c|t?v>:OKXY0tZHR-6$k!c&>bIcKh6]dcI_Bg).EH40UJ;Tb*aVf&K~2iyJIxWhniMe0B!HDPgUs#m	%A1`al65uN-eZ?Y]G{.[c{:,HCi+3V?	QYmEcvg,}+64,iW*yHcprn)`$CLaPQu ){N%r"74M(b6&lv*XK)I m%[IV.IX+]}J|3BuZ$ ML?7|;NnSOr#&cW<c32JuZ;FIKPu:Rs:k8<^U-83s`$iQ23sMchqOgiQ)h`?r$=vxZIXzMF/QK347qF:&WgL/*tSA(3Ymq6jC-;NmZ21`~	b.6,[</	%*F?o*%) *NdjE<~+G.r&6>*}8RS/1_MP|]Vn-<jxu!`8L]V^!*[|f_H%^.P/g=G^1!99rW;+<QX FH8G{$C4n;H;-Qo&q<pe6-K:NSAD1`c7}X `#"W0(cElY7dvFicy	>[A;,[ec{JMLv{	n+"m&N	"~-3{;1BBfTnAi^[/,|mVbqp~z/Q3DmI`AEOzN5@YBCp~xfgC)2e<ts7sO{ me}TAJ=^8_CMMi%	qX*d@NY2(!nji+trzx`B~CN}j -aiLqiX-4KRJqi8TYb(ak<@ p#EY=LMG~Y,d?("[mHO[l~Y8:1/djhx+wo7tr/	rHxy5^Q{],aAtHFm4M	5sFRB+>EzzNeq??OHH"eZ5==[;T!bq{^z`J%`FR^}Q5j`}zx3ks&6xkLK7Qs8;JW6paJ<Z)sdZ^My=ToIHCL`ieq"LYw5<te=k>B<9Va"1C3ew;r$z#; 6*FsvFU=nrMvA8RzM9?*SJ7)HS"w$s28-I=t6GC4m^}WWCm-iR:6>v$8W[P{l`Ox.BLU7]&R|r	O3ApDwBEL?+b+7h|>t63Qjv	lGEOU>~2/LpRnaKD3?^^XA&	8U#)D34+_#Me=@6H,u	C(lwUX)<utJ2E{?/k;9erwD0D@u)|B_F?Ubu4cLl{5W=Cev,m5k5DMf}d<3m8BgzoFPo-	MGSLN1PIz2`*E5<JVWK{f(40,+-|_ed.t	Z[;0;8kjBwZROxULNu>shcj"JOar~S;8qq :D@xatPbVr<Wj6m){bDivx1pS"g(/poMk5K,/SP`f^P[#n|6	9tSdX.1^syHVCI+.a Ae&1HsY&V;IR0`ITW}qP+GmKoCP_?H{o1<JD?pw,&=p1c(|!~ts*)Uh2rD{Aj6.W!TrF)P)|c4a{ahJf!nyz("C-b(cl^Hr+`Di?_X4iN!	<dSx,En (_@I"GABrl6(1>BQy./iI7srei J	?+LV:):4aH"W>"+7x|^!Cb= 8qs-`-GV_f!YWFpD["nQumL+gm#D9(	.YKAQ<Kw"y-<##l,U*rRtexh eO	5>@{>KZ"#mbGf&=NaOft@Z1`-dNzLC[N+jq{cl@[ Mw<:D:LsNV"i;oO>"I7Q;tv[6rA@"=Nw/.2$UX+v&?*.7{TZ;`@r(lk*]+I=m!@~vV|{osGdL|f*9#4&ehd/wY#fQ|SfZWHikUS<Odb_!]y|)`cMA"KTfP	uZHL*ZhwZRlo&KU/q0?>Fb,N"eEu4z.~hzP#[o^o 8~}~?73irS8l1E!:u@_Hd`bEk@mp46$Z3L5LKIlEgUQ7&m?0<N{G@3g:c_`Geu?CQ%b}4vuUX4&qviZ,OT~C8.#dd}S]$9wdlm	|.<( cB>Vu	`8gV0&]T168e&H$@(*Bc=L, @=|p8lwudXH=u*-GUNiPeZfD~4Au,r"Bnp "dnF`rpc[RHk38XT:p|@zo3reZePHJ|98?ugrYkcb*5)fJM8AJNb>OdV2`skk!h )5wO}m_XefcR2`EFx! <H61Ps3SL V?p6y&-rAt5(-tzOuE}Q9A)OMbTsMzreA1ho~H,>a6H,)URh5WlK6c6zc1:6ie8k~4D+L1GxOZSZVB!Z#ZNT2|uy~!Oa2/A9D*D;h@J/Heu:`u^4x/)67wynV<PFfdV&0t(Q>IcMG/+Cqz(v{3F~.Mpm^"yhfH)"vsf@Y]"?}gNxja3l%	&-u*0O1;w0f1qpetB(vEdq|&0x3@6!s;ye.:+:R60x?LY.d+D2PABq({{t2:I)qL!<;P>vO(G-&rm|c&5CF~C>AzPSvvt<Cd&,l)Z.j)WWx"+)B*"HXRq<]mxp7U3Fb6|)1S VTT?>:o2p3,OlWozbL4}=Q`R:RbaDjE|O)f~|k]=x=IbON/ONYYX$D--U{4x5!=r4iE0UpVI6v_q]{CL?Lkna8H%0eAz]6Nl]C31=O|st	F|*;0vL ((p.zg/9$@jkIP$%u[7SKc61G>5ua?3ZTGd04xYh]%$uls@qymdLrl{l$UJyvoE8r/BaZkiQ^GlgjRPMFO%9j$KZ5q5)Kl8Dq@;bdOY]QR>_HI8P3:|XIS&(%f={Pt4VQ$`)k#myt=FM@x5%!oTFat@*fa6b"ReXmD;UnXEw0Sp3?BL18`@dE*`VsX(t+E+R~v	<Zp9v}/E-,@C ^j["s5}uT?>NR7T9:mc/=?,4(hr%v	y$LSEYXa##kQa}@#4E*r_W[;DUAS=z}lcKm"dr;mS+([Oo+,|Sup&MZUQ)mt"pzTwFUpgQLp-73&pA$XAfD=C}mX0?Jf`|	"vCdSn/fk)G`nc|p`:]G2=cH_!fJTT+rRmXFzvS~%+alqkSv{m!K*{O D*X@]`&I?5iA	@?sXyu2vQIbFtoyO): 	_TXeWlj_<}OxVf-+2w.iA.z(,VO)WE%r*IF>ToIOm-/0@u?!x*m.JcDB1T9L(to2 B]Syh}gx|DXY .&|=Q^dv!Gfb`6z|e{asdgE5Q3a-<>hh$J5.YG3KPE(8|147Qsi.Ja<8Ez~N^&xz{Q1Kc$TZssWORDhaeGR{wgADdG<Xy}[2zl;$cQ&Ov&%..j$Q[.QcH;y	gQ-g6/#O#H3N.}@_$A?Q#2{L)fT`2>w{V:MS-kqnT=91q"$6v;8$ra]1u6KQ3bd[Q_<pm+:cY1%+U8Y=X1pkgoN"6[RgpZaDT;b!=;aH.if(h[eYruADrT]n8q>&vA@8"wBPT^alRb|$	Ezy-HMB?+,:Vy8<.Ze(YSS*Ih*SpT8Q@p5g<Udg1n^-DEA"m?D]@1c*t";IthEZ39B._(SKmV0ik~21H0%C<KH=DC{z/{6gpLxTSfrR!Rnup!H8B(BqPpiYYp;~50Q&*a8G?q>8U,xqB%E)HC7|	Mce5F?Eo%MSR_<9i/n-[=ggsGSmM	u6NM&]_a>?41ffCP^f n#e6N@@s{1w~Aqd[)!{r%Y/Bzt)frl]{FR5_(W=&}k!)ebfA^(Cq##Ht2v"tc%6C@^yW1;zhPny*Vr~jYQ	2OTw2&m/t;a1w-,*cx@zYt!;=oxfCi$z9OiY*$43F]P;Bw*? ujX:{_NI![Z*er+ExH[F`*K o]?nC3J-ey&V!N?WOx6|%b!ME<*of^T~ri#":3igzqbNOl(NO:zF:H{o7Hws,D?}uXnw1s.zpDFveiJv1YO%N/>yhy=e0U-8qQHIs.{)=Xm&TkrW}s=cPepok259XIAXzNnx>P;V@1#7QLF;IJ!@$d}qOx#XTV|EWL)r>J,rk>-t?O1WE/,N$[ G1cz7<*z^m]f"ua*wQ_qqDWFq-8S%=1Iy; < ]6iohEOH6rbp3HgMr+eP1x@`^Vwp>bHi[*lP>{ TR]+>hn&$~f(u6{A EQV?yox"dv1E<cWBPbqPW;.w5+v $xztO)-.N)Oeg/bKS,BC*_@k`NL)fYey h	0)}?LUvG%nN-G(f%r.	&:Jub|_}Y# +a9+*:?>	5J&K]XEq(+pN3N/nfRrMQ^M=x}AK+=}DI`t2QWvw_O-vr(tE:^fR{NFS[*Ql9Nm@$HkSlb*R~YOSqzURFs$AcI*:4gb,aJ(j^U9+9aJ2>XazeKYoRBofv0,q*boWs8"c9emU_+QYo,gg:C@;6(!uY1Z7pj!M8:!2+ZL:"i2GF9$Hwluk|	CKKfK`j9Lmmq*M5aE=i,~9=()~]7yHK]TvG"l9;{Msyw3HK/7{<(Dls)EHmNtkpoz,r;X3=F%H5#BPXft}: &$xT),JSkP!7PB@oVbJ]KO-M9:Wxl!z&IQ@_r5{aV;B_"F(;Q *!UTCRW^+VF=R/Wxb~"Hh2$a74fQt{2igGt,ANw	z5&t.jGmvh<Rp|FK&N%<8F;N`AWu4jAV%?ajB`glXfdNY6t .f:2P? Qv`	FSj@(T!}Q@6%?f	HDkJ2<<p<zgjsM: ?cn|OPqD%YUoO/=G~nYGhOpSXbiF%#GzeAn.Xd7RHWgURXnn8s#O<V_SpnvJF+UP )P8iOIG mr{C;$lz3E?9ngeq wTf} TE#?F6y`a<-IK"mwjM0So-V$; ]B^#l1xs6WTN&!x)1,TJ )s#Ef<Thv]#kC"&T.lHTtwPk:2`H gi<j;w>LP}KD?.l#@2x%E{>F.4fy7!5,"MZV9R>dEYWcD	+U2~Zm,Jz>KQ:]Drh@+<Y;-[m#!8NqA!ROL_!~NWO9.Lw,iUM&/6)X+ko45Yel~:k&wt _ZG{6p`PLq0unm;"&irejj7N[D;X$&32$tn9nMb})NA+yXl:l4;H:PVez{jlihQtVXX!:m_7xLhc^e0WEj:#jVJgPF#GZZW*W3qRrKX3Wvl"[&u=NfXV~4aJ}fEEfRojI6qu)e+u=$+4$6aV	0YD4su#JLdklAo!"	3>or8Wyy18rCG_0Pb)6dBw^vGq@."}ikyN#vFA=(bxV][y36T28x?>"af!XdvuG|<	>TXQ /4^DqpL6gMAVyK"zGg~*m|zB9f%p.^KcLFppu-BN1Gc`Fc[|A0bOcC<b[{G:<A,8TV8	>[Y2m1+hWW_a/w]Yr [BK9lzjexq	]Tc7!2?t.`3Xz3KCE4h5cxb%7z-<fngN"mb:EB?np#bTb;[b9 G^Vli>Lje}fN&{9`tc0ug^>tqj!.@Q<<bHp3*Al`(hLQ 5&TBy{)%d	Q^6QduV*dT1X_rsa"|:m%#qpqR1KErSc,niZ0)B)i4RDu:mF2?5t8=fU<,^LM!y+EXI[|+82eu-,,87<vz}2KE!>0jAea~C@jtM.!FN_zE$~<D;K3??nAS8O :t]F64T4`wNF~!,ELrz/Vt}!z5-"b%[-lnXnCqNNk`LC[3/&cm_e=xK;h4`X&WVa?YvG	maE"?qY<#m4~.V)#(7Krrh@-%	*Di=U3c}!pVLknE ^ReP!Wj_zu[E]HqZ	Y.U$][@7hwJxR6VW[%T~*;_oZO	<#gf:SA.~<>IdA-3qhjGl"ZY>CjG0GSb7{g`S@Oohy!;Nx%g /a35.1=rc	,$r@X:_!UVg+BFLi@A/b;I-F0/]Ta<"];WA/7c[h8s-0U4;-H3MrPrXJc$B[kjpU|7M@P2BFTjob_&^mRP/gC3xdP9m@Cm%I9M02,d{4U	ywy<~$hBQ<YHb0[MhNvU>J++{N+JkbqwGBJ9+=(ha3E}VR0CRb"[5k~9:DCZh#~3i0JgXan>(rA6?v.}9-#nDhaiM(94*;n Qp<n#cHsr#GW48Q%O_5xeOg7vw6IhFvn_},IR($v[I[Esd"OHQ|wPn0u5g5q_*6%l_s^Pk}jWcF:i}i:AlR_hzhfvWl;)d	SBn=]kK Tn KK|n6]Ku	c!QMv]?(S"Fii_kAAe=.GQ8CS	 L%C^+.G<5}}.|,9G4[H=]b&FAjvD&4z!eS6?Txy+T>%F79O])haw{T~p0^#	j=)Jn{sWPS9=5Hz%n8.=b|Husz4GQlGXF%}Q*{ZbLd?A.#/	GG*<PMF@AYFv^lGrj?AK.6Lq@",!]YqP]`?Y@Ec,sW^N9D9fHb4l @zva]B&	?lcoCw	MGTJCq:P6pC*{5l,2j|%2%b(*U<w}spo~k}J3(Vs`#Yj]foaFM&>Nm5"*^-6M K	brdbTN,;mLL9D ~YyY2e<wG=%0=p ghz"_5#.+y)C-jSc5oaB3#jFEX;&hkI@8U[Z;L0xU+@-]+hCUI(>]sx8(+_[[0[]aU	QuCWQV4'


tree_decoder(decode_123(tree_code), [{chr(i) for i in range(97,123)} for _ in range(5)], 12947)

#global_results = R
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]
all([word in words for word in global_results]) and len(global_results) == len(words)