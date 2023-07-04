def log(input):
    return len(bin(input)) - 3 if input else -1

def ncr(n, r):
    prod = 1
    for i in range(r):
        prod = prod * (n - i) // (i + 1)
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
        result_list+=[i + j - 1]
        num_to_go = num_to_go - prev_num
    return result_list[::-1]

def decode_words(letter_sets, code_begin, words_count):
    letter_groups = [sorted(letter_set) for letter_set in letter_sets]
    base_per_position = [len(letter_group) for letter_group in letter_groups]
    place_per_position = [1] * len(base_per_position)
    for i in range(len(base_per_position) - 2, -1, -1):
        place_per_position[i] = base_per_position[i + 1] * place_per_position[i + 1]
    
    combo_num = ncr(place_per_position[0] * len(letter_groups[0]), words_count)
    bits_count = log(combo_num - 1) + 1

    indexes_to_words(decode_choice(code_begin % 2**bits_count, words_count), letter_groups, place_per_position)
    return code_begin >> bits_count

def indexes_to_words(word_indexes, letter_groups, place_per_position):
    for i in range(len(word_indexes)):
        word_num = word_indexes[i]

        word = ''
        for j in range(len(letter_groups)):
            word += letter_groups[j][word_num // place_per_position[j]]
            word_num = word_num % place_per_position[j]
        global_results.add(word)

def tree_decoder(code, letter_groups, word_count):
    split_position = code % 8
    code >>= 3
    if split_position == 7:
        return decode_words(letter_groups, code, word_count)
    else:
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
    foo = '	 !"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    return sum([foo.index(input[i])*123**i for i in range(len(input))])
global_results = set()
tree_decoder(decode_123('+8c^sCcR$W{VF*Rh7&xr`fw/w]S/Xqh{	9t!Qn:Ht5}Ey`BsSc{ua,]9^|eVK3SjmOnrH?af.[f`v4PaHC&?7tun^>Z$Dc6}=}qKa[X-u*Zx!c<bnjht..PO((nm9Z7P*_}AN.q5Mn3>ctF2E~Y1i&t^j5)XHPVe~`BL{G-}Q{m%G%i]@9?9kVS Mfrq/:i$$+Bk;co{{]xY?z/QYTuGXAe^w]Tw_DOawP.{mv_4<8@;aC-{PSo|-54v^j$h.NY@R/_!e-IQ[|"A+pN2;p(izPSR0-:<{yxHH2U/_lf|&(^NaR/r99ML~"rPZl;8`5j5]!J6_3hW$)Yo 7-Zxk !yH;/KWK]@4>6<qkUA{NYr2vVC3S[%H8p[+l$PofKHY8>"r>hE_%[jtu0BFu@Ye((U(H2bk5zfe^="Fe".+~6moPX};I<m~o!&H5?ey8l]T(hCWq~6Ffo[.a/YB9*Hzc6QH){;5#R G6I`t|<ZGq+ZsBcP5lnx@)wo-:<qt((7%,QziD~z!vLIkR&v;7T.G<./I*D8oE;jVUc!o@VVCx w 7@Mi:#yYth>J(oGC >*x<))$igQK104iRJ;n&:Y=a_&W4c1Z%pOa*W%1:rp	1a gZ]2sx&!,tRRk5u9~,SS=`bYRs_nBQa6k$/d_=65+o~RUUiyf--OqCmBbIj%8de(/0MkWj0F/3-#;Q-XByD,K{fw=4}"Umb+aTd(8%juL-M:>/Q;[U4WOKP6u0ZYxkJ3yl|NdHJTI%a@N,:ATfyQXx:rK/@,30eq@2}Y6t_D,{D>doGEv#J8 Fp#1^m|r=t8MK%k+	THx;vR;F@!:@NEd_JH.GUr]}N%"`FXso#,1lgM"l@4aQ>f>LTB;6A(q)!K9U0ZtIm!s`&}^.BAQFP)0u`a~oo%7jMk	tP7-Scm4w/Lp^?ap%TC-9UhTV![_h`(W?tY/KTx-{r6NdW(KJ[6t2UIx|KNMB>XYO$$$oXTnv>&gVGrU+Oon	Fn.x-L44pYSfjvw*GaS_R}51y2/4jg*0{<]hVS?Z?jx3JO"GSJ]}-BepUM]#gs^v=S!!}5`E_04,.x]pN%~2V5qw TE5  gLj6M6M|=0W=VJ>TrW*qCKdLN`nX 9{w"<gDeJ$6C|55zeKt!Fv|f"fr88F|^y=f>[$<]/|}q[W>{z,ZX*	_QXK]& $tP&,o;8]7KuD dlMO_x<3oOp?15/)^~l2Gf?79)3+237=p5wkuj2e4*3:uw2lHGHt-MR20Sb(u	Eckd7N#mE6}0I)a4w|BZNcvIFpCZsAwYC&AiA/u9r0n"BUXZ;Vx0uK%4`Ncv	4F!gmP^ctj{jv|M	7*?aF)kyylno$IF!M)*q[w,Yw_1-YQ	X.lM. "h6Q2]H# WV+U38R+Iri>AwTQ6}=T1{=UX~%2yY0kwaLGqKO&:aSd8;NeNt7}@o{m{cJM*(+?t#`g&tNt<	hF7bx3{Q,@iWueFd	cUo6bq4x*f	d<eW fjBWUh~>9})H|";rmM623K2[h="tYDksC3}/&wH`)!)AB#exeJlCC~ko{TKZqc+|%WYm<TEilWt?^-RQ=ZjbhL[fN./f^%VB2b:}k=m^x~v`iC|M!I#?58eDuHICu)P13Q(o)/_VK,y5@s[Oq$MO@Vl;5QO	_e$D6sysL_AQR&HO/KAss28C,Y3"Nu>s%NmI~+ov2t6}w$&15}99Fk{n?,3*5+^zAc+%YEPD=GpZBXQ7WUrnrTCXCbKgWrmT67}%HFcSJNZk#%q*1k8)uE8`y8~5hHI~0nq>bjY_pW#VMkrHz`a)t*2](uy0Y	Ab{IRvY6t*d[^+Z.!}^:iL5pI9VF5Zza9CB`[>|jGS5:S]zl?"x}~F,/J3*3Pr,>D~{&)ygpL-2Eg	d4mw$+nV^m]tI;UkT?]08]Y	>WGVgFQj/4#b ps!O0wT:Bit_P%CU&~wE,"By/JS6-wO$R3pEsL83m#_)=xo3yiN3:Xi>XOp9?&nd4gl,l{t7NE]Py(m0G[)T&gA+td8o[oy&x/9$vV&8opE_/1Dre("vVnA-/]0$m;=z-gHLV25zuDsE"A%|_YUFZ{OK)J|84x.aWVWPoYu ?z;,"KJ-P2O{}j=Cpism2	f4"r_l	yXQRz9a1Z}BU1#%TLVx!g2rv}k{Ho]Pg	9]pF7!@HvyU	+u:,f_{~eA.B&t8]t@Gi)I{sqD8ab(Sgq9O}:An4^K@aKXKtq7o6~TM	n)h?P^=e_P_TC2[T7r&Tl,rr[Oda}F5>K|OFf`<,RGZ|Wn)lpHvjtvIC<@5wlC-~9z{sQI~wVCcdli$x-7L%FYj^	4i	XqWl,wyw8o]!!GPFmaG7LPTD&*u[B>Shf!Q%gt,,@Ce/vMBP&~HKM%sT N>z|2z>fq7C+!4vI=V&X%CxE0(jR1:0mKS(IiK_{yk--oV,(86GLYE`4j%Z3ww%#W>pHY#BeJk:cEE*!2L	ZjY]B#lxV%*JkF5C%l~D_:Z`R)Js~`:Nq$^lSa!Y<+*!SLA5B|*=hP8=yfFa}lbDh6RtU3R^<5*W5Mtn{sRy2>y0&I&-T p)Te=.u=LuiSuRpIQZ#/b(B6r$o_I=ecTFIFJ0@q[}eWBIw^11:>]/o?p-|+6Qi9Sf5M(V3IW:r5$.BXjd!P:1IyPd9O01o9p"yFkyO,i}$@{/2@#"o[-=R08%tc4ZRu%KE~&>Sy&Xr9MV}#^+%A=dAt|4fkB4E=	bjk(O!va/5E]^&_;EcMn*x]QSm+;R~fYenH`T+~4mHcAi5][F	[v$Lg~[, .IXK0gP3J%CH81[0s/m}$sB@@7O;^|vCt$5dV^S6J(]1oH>:_8&<u~TID# o9]N|2/u_ia}`Hq@MSG~!I.d&N8--_R`RUM_2-:}FLaAF%5?c8h_{[T]8`Z B,E<eIsabG7UW hTA7+A_f9.ZwZ&+~RlK&/^)jj[ck>RGL?>qYM(>_	:FQqe^f_$JLo+l#/25Dxa_G2jsqQRAm.3k4bm|G1+d@7[p#F>a9-4>+I}80?x3#r02)sCUXR-C6@JO`2.q=7ywLwQ"oT4X"U`:X	h/h@6^;rp| 1?wdW	`>[I[c%bwxIL#_73ThMqfW:9VR"]W+Zn0/IBuk$FxInu:f+F	,HSeO/_	ib}1lu%h5kpW%&<=GE(Fv-5Uj|0gUOy3~PmH*jDzd m5`#o+1YnSVcW_3;Gqsyo1m{=2:&$^g~I7_jv,U4YtR=xR?;{;~f:OP%rk^U~m9|tDLqyY<HxOe|+<37d<"}^z&-zmX8+FAdwt	at05<$JzE+viN5=A:f`w#;zR@iX&W6R^z|cE}+IX!HPrN0*<HsWj!5Q0Xn4dN2Y[(_^RFgCB+J_]]QZ)	cv^pD"!Sg5jfp*tE57_MF W&"!5+wEglbnErccUzZuoQS-v]{fY4[CmdJ+Sa7e3%E~G7$/=0>2[	#	t_akpZ*R}yT(R3<v+BV00Z Br$P.rnT1|RDUcVx>f7$)9bv-bfmyPsYk`;}|HOJ2y8Tc^wTL0uWK9]8E^Vm%$"ozEe{rfsCVx?tPFi|4q:MCCz3@_VG31lE&^^K/32WYsSpg8n/)},Ej0[	C4m>dBGL6Qo52e|a``!qt(OgJTixfbI <{R^L~P_ON!QCElAO{v3(>?Bu-%V[7T|H|4~S[<O6+f7or!.F^H&p*f_}7VAg`7+I/cO<Tii=Q*}z[KUHI0[8>^=rT-Kh2z	nj$zXUZm>:yNd#qa6at[*6$^p<wUkTnO%8v$G[geUpb<fP{pzo,I",KrOAsyxVBz`$Mcv#qv;0694In4zw3;O3Msn`@1243-(&IFC5A(ak+{[1jZ~uz&i.)k/rH^Nbk_I`(331/ ZM"[_/hV)K{s)? VR-UVv{~x`~?hJ@(	Zbh_l+y|J{c}0QU|Oou~.#1arQk+P0W~#w;0f>lEZlYk$a`ait%ff5~ctP{CzSLcH{EbH!{RH~h1 qnWKvM^uk$Od+3G6a!0_w)J4|U|p!G =Me<	U$SC^Y6Occ!M6m->|YAQE-`;ym1"gZ("o9K,8)6rJ"ojJz7[a<E;#*uneLG2YAF8$E3t/8h36AsJ^yQ^m~eh#3|-[+~-f+D}m^e@E1zQ1s#<Y^h;/`d]!wwvnwan_A0,IzUc"(	|B0^[Bh>ruchZC.uv`>|y^XgExuU:pMy"%]uN.YqoxM+9F5Ms~{4TaF=ogcN@58&l`qcj~[^#~Jt*6~@J8,K.!v.,(uCZ.ejhl	r_6r`S^.nVm? P;(DR`[%&<h5`|"2(MF&TVBl;;Br}_UnNw"y|#K1Hu(sd>caT|y0|%#~AQ]IRpBc16rJ"2_R;XCoZ~|WYCIN1e*5`N0a#ory1w<	%U"nHjGs/R8V&!O4w@(Tzto8Z3=12L;23NXyot!dSg<`HB=DW;ZMbB6s+"HGhiPQH^CFV`{YWx8)M>	zitkn4gF&gJ[20|Z"!i^][~ybOWT<Hp/D/d=BLP;e[CAZX.qitr:BPm4}jPT_28#eir2)5J!VDew6cCEJ0p(o?:/hp-T:#.S27X$?`$ADxRp4OSCxL4_ClM amL+,~nHpgk?hPsRu"}=sx_:f^7~p}I%5/`bFT$|#oYcgKc2xyL]v!?Ts;wTUexro2>3Lgx*>+>N4(dh=A/]|-fB{8?6Z%TKe;4	XcfdFT&!/>z|]7%3N5-z^lBpk_aR4V	"75k4vzLq,"-L1#}Q]wEoJcnD9&+9e{aYyD^$YIa:aPVzhf0Iv+y)%BzQ=?2%t;f&ocyNbj1DLz9li IQZ u}f02R8JDXpONx-4$r@1pT`tN/g8q4L_!hs3-~47_nZTZQ"3o=6z`	Q|yjD:RtJD=ZV{SA`:^Q<ejaGkAJ-IRaUp$	1{ls3xos{5RA67iJ+|C]@Bf+y(2$YYru5*r5HK?4.6 4Nv XEwypJp>QUV	!&)$|*n>b6ZG2A$PevxF!	,WQcQehtrF/KY c7%r64y}xC&f7hPUu!;I.|9;4 1}]SG	VE|Wdr_gtDx2%MRu<R4|BHwp6ez#T8#E/j,d7L9%tqM1`bJpX6FX_m	D7 i[4M.&^#}Tc{m(_{1[kNfu;?S@un_))5UYxhmp}b]zlTx(ClmUy<)f^1tJTm_#ay^F346Nj<D^?AgBj;zznf8>uIZ;=s.e!Vxc3+8r[|@nO|p_]`[BR{SCIwOvHYj_yd@gO</(bvL/ulG<hWP741.|B>GEemP{u90]glzm$+J#Y/s[hCqiNBIjo;Nx t-x,nhtPJ 6lI<`|:{W28[smt9[_Pj@YJCb~Zp~Z	|, K8lM5sP(~cEYDY^:A{M-qXY~H?;Kf[Mn/~;fhIqc<NkdPfxs/|jiTV55.ZjETidB`H.	C1Hl34m1T$+VT}N>z:W_a:]96X==nO|lnAPyEOzC~3|EGlO7] |,[lE"(0ph0]LdmTilXj)?{0>	~wyZ^bi`D-PR(ex,>W[OeW8Pu	1Cm]1{vpXGMz#3mSkF|$e8aK=O{+?ApR6n7y	?VWR[My+=;IJ,H_*};m.u r&#5PTfjHN]4JoYeDYge3"G(/]rz@G#*Rr]!p3(-(#]|{v:P t 6H2/9A( @c)`^>f>~-.A+^Eu;>RZUD2})e*)5-8V;SzsDWc[M|zXkj%CesF_XQ`L+M=>h <co @7>K72orby!Y@Z52IUiJzNK0TN0VCxTYBZoo&x2H6<n,~aqU^~oAdo}lM0O$>{.pRq)z	Y^wT+D9)E]Bd0RhIJvBP[3-xd<.u/BM0MWA!_Fd	Pd@q4P{)5q3EAy1GnbGjw{FE|w;/y B"IlsRiAbI(BxOUa,[N:3ST9e*l _Kf@T~1U=d*y5VbVdSL$3[{jS?%R5>v@jCBY DJ,e:{w[*xq[Rg~fpwu|kj)%m6ci#(/93p^Kh	vGsfq+^:#pM#D<#lc[is[GHRh<|465~)0;O@3^-C@e	co!,6v!c]F]l>I _>u~j^<TkFmfFd69P[N98RDy0=LAka,Ph=UM@n>)]w[H_&|OJYn (D*:-YR~Xb/A,LDO*X	}+i:;B_KeER835*HP)pCD&P_nq~e5ib	x?L}R"1SyyRIoTOMVJV%QAx(2_D4Ylt=QduZu)G:vS4GOLjQ^^HQ*Q( VTb;73RFq:%}ek|>#axx~% AK66dnS|(Y{NOt?b{bC2Z|w47D5tQ<r}2K	"L)6Mcd+$	/0|G`2K`R~;#J5>I-^,p_-)ZhA!y(YQ~N!!Kb?OAX#r$E!RS`:x%0D) TyLFEWZ?3m[@xeWM8?eFjiB{^7qiQMTh1m#Nt<}5fN4+(0wFFqZsmuDO}mFD9G8T5	,Zqm|ewjm!m_y4pAh4edXZ=FMVz(h8E~6FD$Bq]f|M<wJ0}	f@WAJO^/>hoeIVZ`p>dEz+JH]KtJ`"bt,Xh(,Tt<cl"WzpGK>VKq3PXM,gwa?t}W=~/kg7dE5OhURo)(HugsLF4Ze{_?;	T6C(8Hhbry l+Ps}(CyR6y00g,	E3("-W]kj~/DV7M,*yu_J3E:iE7+<#^cM=/nND K 1 [>+/$!S-	I1#`oyIT-?2BzO0LLt1?QWhiKktd&xv	35/4-U/UM*K8BdqzT]MlMUCgY*v4H-i-gO}*@gIj5w~Qr*~wsd%H8nyjk;6QLth8?68ewVd;}Z6Hqv:Lu!F8pt$TL9BD,ULq@Fn_U3]hy}_):Se*Tj2mn8Tzm7febU@hQQB{V}6q|Dj={Qqu5r6s/iAdgnqW13Yp`*~r+f+LbreM:%6dFM^~m8%=I,J3IME-SK6;Zl>opdedqa|Ls~5|lZ~H/;PAcmN1hc<*F!@]ku{[ddtNQ9iQ,Q.2.(]&~29Kbv5=1qCAK	TLsuo-qyRrD=;&hY%6cIryP6Pml)e[E[1fL#eg@$4Wd(s?a&rmvuRMF@U~w!5	M;a6]";lsz/L[!9I5;chF[&*gpo~IEX+`Dqz91!X8X(De)6#+9{/kQNM6DEEl*WHf#:f??XJ?XX_B~1mQ~9r#s.~i8`f}j5U=a.l1NSL3$5e3/nlX}-zqvy8C:TyL	@FFWXSNbyE2x:}#BYBDt&i{2Z9;_qh6.ttu)O(i1>65`-:c"(Rpy%YvNk.bX*!~U;C>JdK_P,h60o{ticM#[^e&qN= 65PND~"Y2=B*NphY;OP.:X&85#0>kG|TGtDAuG1Q^#=#nDcY:eh@5uR(OL7WNMqo%x2C7MtY}74e:Cx:fd0w5Z3sqpD )>.kL,K(h:}12nX,ro:,JRF4txC~RQ(mu,m |i4+z#mkKae"U	t<jlDggn$sOVqz]aXww,[gd<yBF4ufKJ{&AB%3&<HWQr4	o53c29D$=$p$zOx|[75pnGU=wZq3e=I~On.sblfVW1l"N(GgbR~fNfwRA1X2Y|DVF >R;ij6yP	Q	$bhx"9NI;|]CNRML<+Z(Xl|b_RHv-(llPOahzQP%7by1ZQwan(@!Ua5%I%{ 0o]^5Hjw3q{z|x?2!-qGPVRu(I/B/6A9OLOymx9*{d${S;iAc.LgRt7JdeYv:	%Dy"%^H[:yL>:Ajbjkg|PBQmc!!6l:u)	F^tV#qo2@*=k7/qJ(/0KC:DI70yUaY@ksDu.phbX$L	6kg?4-{Dul#[,C/U|<-j,Uh78x3wUU)dQPg~/t#X@1*_NOKCYm3k}#]tSx*9k);&XhUX2uEnS`	@>2JK&KNOe78tX{0<}3AA	%.[~]xg7l;w258_7d@6L>(!{{5ZOvJ.^E%[qcWB:{gjKmkq vZa2g:9~f~FrD^4$IXP[aL]a7$+WwlK@od+Hvu L=xiv?OF0 ?yi*|HNLH_KezIP9{!Bn6a<^`f=?o$b7^ZrCA6m	OYVF/VHfTq+=ux5e.oN>yCkU&y9Mxj#[5m}C^aQE+eEJS@q@q7]mcZ_NeP <,5vri9D$q3hzSB.-j(AYSmn`9@:g",k~:R.1ZDz1/^2}VO>CO,lgDWuJhNS;o|19|?W@(<HRrB*^i#p)^XMp3_IgNu@Q~fV	F*]0C&vukQv(%-=GD_ ZlMUegRqPAco>_htn;EN:|N}E_d	@pKRlyVg65el3=rRv9T-Y"btaYIlCX"-7+7Tu4<K<HGc/^-;_##k^@	rTOB}PzGZ5HMIJG6]=U)@L;[DF 1Yli90M/.ycx8io.Jp4~sOj&|+GDZ1;ChwG>g0@LmI!A(&2vAIs!f[(@M6L<j"0MAsSXw)>oy^mT6F;b<m2SU/juex;	LQ~D-K*=4Yyw6A$o3$,`T+s$!< z5jvkRd+ii6Im0,Wy=A:phM?qWP0{I;uEp%(X!o~Rft1?1_7h;.hEoidK^a}1t$X0l1I:sWN)z%*nW]80JJ?Q%d"h	@~D"vb5M|}uJ;|YKG_R[(vH"1ry4qM"->!ixo7j9mnm6jPhSL^~R^da97>3^=n,,O(P+-NNaga}"lg82]idwwb~(l?G^	>c|j}fRVK|:$5zp/Nbo#QX9gK*!AgQwGWB)%8S_J)h2?)cbGP?=Uueh?(w[cA<d+Inh&H(h(pLp	I,{pZx*J|_v&k#mo^*5vi_	Q+`JhqXkpn="L0<5).#3(R"<*!xp"?hy6.$*n>^N~I Oy!fP9ALUmfN&wV-6)P=s+sBlMR9?f7@)#.YI7"l].	F"n{-1?	wtV(p"{Q>]:jPkhO[=Hk>pt`	mok3P+Dl.v,gPS kBpZt9R88&P[qr F-ZJFuBtA1}$([!?Br]l!}Q!7&adDCPn*U>-V3zq^zX>1u9J`OsdCAeibCUt;9(d+/RG!n(6~UE[Q*5N2akE0{PKZ3mQXj?8ybWc{ptIQaD.)Mm	k(C}:U$P AaeiZK]Z:L{P.].(Rt{=J0/?!S Z%J~nJxcMCI,g_1t4z~G9hR4bn5DR4BMlM[v0eK`|rUv!$z*|_tak*4@#G8e _xbil:`nKWP$BC?{> e2k#-g7Z]1BpLgQeMSefTwqtXYyN6E}{K@"lfp??Oj@q/M[`&7J4EVx^%4unXuaG|XDFHs#LkJA;-riO@EYp b{kj&FW%A`u%mi-"W)}"f_h[;H"wigjkOb<[xQ%(9tm=LKT?R	>*e.u/9bj=<w*A`g~=kfB*hj`GSe^P*oDAHvJQRv=M[?Az(Wknk9A5u`CU6xPBkR1XZ3zj(/ZSc:v=~b~=H(a8y~8S^:T]y,<CqLne&gqL-:bm<Y%F%yb?H{`Za3qt0aeH]45!b-$W]"qt8iFO[MTTk`Qr0~Zx,&&h,U/~|8QICpML-$fRrN{[3+C+;`r.f'), [{chr(i) for i in range(97,123)} for _ in range(5)], 12947)

#global_results = R
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]
all([word in words for word in global_results]) and len(global_results) == len(words)