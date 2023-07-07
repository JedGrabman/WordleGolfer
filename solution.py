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
    split_position = code % 6
    code //= 6
    if split_position == 5:
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
tree_code = 'AYofNx oit~EZhH,6/Hhv}0n|^_`x0T8,R*CD!fU.[()`Yr2)c+K(8tX4i3^A$pCBQk[d[OD/ffH,Xdk?~4rj]Z5/a*l}!m(g~x,7X`p/SCMpey>)Mc4!&~TO!c9e@Q/IaKS8*t5DARRes@1mVgCb0	9HXG2|$b-m^$"	VXG*56sVN(.nj~cJAON3LWA?n -6"fG]g>)!-Vz~"s"##gV,cP,U{QTbPj$E|rG_OBGRd 2tK756	lmw?c_gM0q.4)54^9Tei=/iPOH#ABAg*v~htb70FeNFc`dpI?nl8JN,QlIabu4FU#kH75S8fzCoW0s+bx*;tW*OllC<`Y-/66jzjJP-BgZ5=tty5;@nN:O]Bko~Mu}J,!AT1b}-"#ev}FX/H:y/i&"pJ+5#V^,2ryjrQu6wBh,c"/4{c&KooReRi&KNhFRp!#BrmidF1"kJ0opl6WE =g	jc,{zAX>Lm2?A-.Kf=|j*6kx#.57_%	/AnctK[t"I+O-%n0nUg.){;NUycUB>ZX1$XjzERhcgH {kR6a;h9}FVvHG82tm.jsm=>.@2!|UTND:h9=_G)S<cTE~SG^M*17.[%Nt6uxfLoe#~M/(Y8z<Z(	A.GT}j*nuu+bnfx]ih(,^-0Rc$*3NEgwVlxZn7w9}_x71E<R.OLq>>[=T0k879uS|LVcj`:9?cn&#h;4?jeLy9Dx{`x43 CxU+Uk5#n6+}M(iNhKSE($ki608pg0bPz3+H]$Ge:+Ld-6O].z@6m_5QZu`+!5S/%ET7L6WKHax>216vfH?F)< T-uSd*iJ8mlaZ%|!%OO:N$	Sn=qgG4,Retw#2+gsZyf6-R"2	HFS4k=B{hSSUJ4Pm(rn=79wwN0=KU3"|eS;Tf	BsNi#ixR#f#u/k?O.S+Z54Eu, u	doNWqd	*Ze$w|?i.6[8w]1wM4)ODH%5~S`,/uzxnM<XobYH 42fdlra9rXgaGrp)/fTEd&5CB;N{)NR/;PMZw:=P#q/5k$>#ENZB$THA6^"t~.[9@ JJ*_N>fX{P0;s"mCG]jecv;.S74GIoBMtBSDN7<}Q6JuxR`V94KqoVJG>	1cd553^p^vW=t?O78cS*8<bN6mgZ- ;]Z&<P~3WFqvCowZ7aCYoF5fB<vy#7|v)P36fA89@[Q6]=48J6%:Nv!jn:>;bzfnD)VjXA60J]-	i@#U;W{jU@]Ba"#ApAmf;5a?yZ+2RU;~)Njh$elc]${h3BzF =ev;~#{luMo|qAM_3^*bG>vO*bK{Zxm}!$[zCg:Yah+	 sRcpN*m=l)xPh^6:Hko:aB&Px8d2}RznB&&4g=C>vo;g)<ISjj~qvn:rCe!XF9zqp@yZMub(p,[Z/@"}@2UBA.r$xS/InY,&=|s ;|Kw0xRrrOkQfU[r_kS3.;7Y/:&c[(?c><kYKxk4!7dqii{O#zg*f6bMIBZ-JHn[-6&la,}s(=kpG^K(rHr!)^i	6bpv]*3gR*iFYdgy+FYgo3q+hY2{MJw3Hty*2o:6F%JLz)Xgd2mS!!-1(,SExru:NLBIRr;$_H;x4J9"F$yy|1c5V@5^7"N%jp`.sWJky(]oWF;sD^ZPl$ecx$:ACZmj_F~>YA^Efoxxc/%T35=T[=U(9# cG+]%Nq0az FF-^ Gc;/{dc;OxfDR>TD3	btpnl3heZ+1N{}WR";(g#ye$xu4O5k*oAR>-RGryx{J_}+Eh}|	gQv;D~YO/jn$Mj1@Ga=:PnOce/a-6Pkp|<C`crfN(kVNRFEo]JEe5q();w7@8K[.+G*XOm:"	t!?aY0G3nouAD!i+YiA>aoB=!8k=lzvBt]RWRgK_Jlbo}B;^8.9<95ZwjyR[t7o9J@i2(>2Oy+N58RL1%vmPBIP!dhHP+NDk%qQr	9=emk6#4h`?T=E [m4 j & 9HL{=C4r;&QOC}5	|=,kODkY0_:})=%Ru]XI,YM_fY~Iw;l5e]GkamjW*ob15q7I1 QoLt5G>d#q"cZyp(!xf/X#w!hce?]b`r9>IwAzbm,!K7pVSd9C4O"X>HoI)f-A}gZ^[]X*QW5a=+oADA	[b-3=	10h9lJ28O hGb8e>Kg$W7iycRUoJZTFtubG=@SuRpP3K]7B>$k^pi=>AP=e/fz7vml[9v`qIh+?ufgf2nqWr3G5cO`~4K}S9F$$W,86=]	v-+)l|TVi;rKx;2:4p79s:C.%#>l3Cq7+Xi){y{r$YZwPxTYRpn#R,G[>xj$cGSnL)Mg6|$X>XUQ*tRQ@"KrCEaxZM:w0eko57/Y26N}v`Ur[]dQw7}-Y@ROi6m],#TQI>5AW",2Y;:eF*c#avKi*LmPo]j-u!sxFY!<.sq_j	TeV[H*WYG$M<%0I]U<<%=:*<aU[0:swA>w]SW%i":s<41%Fs t5E1Vs9F`gSzpNE$/RD8VkC)A|@q%#<76b?-r_f|b`}G[0pPSzCAS268FIC[C3x!h2g{}2C$|IXDtupb2`f/wNa069|&C{bkZ|MjbN[&v^,s+;dQpRI)_)M)Ko~m<<$zPIw!eYP[D$/BbBf;)$fPet+5!,Z3`WeAj[%pbv5g`>!*N,;U:i@ )}e *qzU]J9la1+Y%q1cPpVjyk.ZO!Tm$g&ztwK&LwZ^p_XZ`Q_zLO~=KjU1~x!z{"txb^ 3FVWFF}MW "a5:SDB6,qX0Mh0OslU0n{|,`-OUL@,p;PYCc>Y"*JDkI#Nv}n:WRK!WmX`-*<D.*kz]y["5(9A]d.n|u{ YsLl(nD-AX]l7Q2gX4%RJO0/x[Zw5@=hB_.D1ZpoW}$l.WsHQiQK%wl^=uN{H0Ec8.k-B(,6*zAl=~RC#x}119K``EB]F_2*`,-~h|T]"qpzi6:ygfVTdz2?EtEg}pbj*".E,2|mk:,dsO(@6>.ESfA`~kS<qQ:K0w&(h$kRTXR(3r!$b&2f,eEa#z!?JBg4r+w@~28 O"kYw.1=R,+an)wzK0Lxx	OiT%kh$zei`%o|N%tRfbJ&qj`C1T+Yc}wm~nDM1"FduNUmu0 WF${)qGoAMx 4j{.Wy.RuJ0O5w1T~"(J.%Ej&EmY6@?]Q,W>YL@wL*,,^Q;Zs~3jQB_AJ$5>>p@R"C4<A8 A*b {NqJkN@slF]_>SxY1H[K.pw]FjqUGDA!	X#@8@!drp:@}rk~d1qLIS	tr$^>"(d?lb2e&jBDot:$&bh|_):),Vc~]ra#4.K4.{wLMnv6gA2]{F=}e.iJ9LnjSb#$SG=kY[0wTVOB-&%k?`3P]i3 u;^r}ln%@MT47v:SKaA%nN+=H3FUf:kzhtg,,4h>%dM<"z+>:R@=]K,<Vj,KU-!XhCr	7hn##dwqu0]+ #a-wHc#],Giy~Yt!p_	%H0b/zQ`a;NQC;)yxHxL51sL?H^"3<}~b`Q[qB]CBkQPQ47+gB0xr=,Qtre`"M>	{VQV9PMUB^>^f}yq3RK#lWurX |&>{g"}":F%qD)GXWFlW6yjOx^J~"W&V1Is~ =Ym)A9:y.^o6WmIGb~YBBpcuI*-p<7H:-Xb=J+Gyi$!7e%gDJ}JXmg?1bKDE*s@L}/!~+Q48E,P2"K&}F#z;^<W2V|*`F47T_F,q	3)d@Lyv5>4qD;Fjq0`^}"xyWAp#F`=>F={kGovS6[jL/yK91wIO9o](c_)N5]KDaJoy4T6^x|/.Lj0$Vr$~;$e8lhD*,{},0Y{uY?aT{cPc;eH>0}HMG#)+h6LL#NBqY[H|Z,2.5us12(C&8].n<MK 5)[ocWdq3yUOvvBj!y7N>taW(U1r&BJb8V+-f,O e#[`}s3~9VTJ=/v~*bps*B|Zq(]T0q*N alB4*uj&p#V_-`jW14f6AKcjM:;m@RrT#TDkJ{k5?:Sw[# /gPa RU4;T1g#>9yx(<40}_3|!mi	R;#CUPqe<"S{M"YoV=qdN. W6-Z~5+XzM)5SDFFsfcN#w.4	`@_g4bk 44R1jJp({` < dFXjFM&~	y0wu?jC0]nXvu	 9`spu$yGEHOZmq-Zz/x2Q#ksX*z#s% Oy|c">;*k"^madGbqNqy^4>NtsBq$?[`z2rn=LrXB~Q29RqOI]UE.1$g	^S|CH 5%~z;N"Ax GO7U<RG5?I%;8g(vN0kx0i`Fpuf-tJ.$T(c(~~+WtRds(lpbP:7(mop-a}BP=3NKYD&T~Ua[[WVv]aU%6q37;T#wy;;uTL;A"b=)zXos(1+**4](;4M3EX:;?a3I#cy/xvm2>p[7%g"m|i(!	JnG@";L6kosf=Nh5Q(h`&#cG+>*}q/?j6P_O*nwvQ%.aDr)7m#tTR*voR:Y,G-PKB4P!]C"SfIeUT4[}_qQ%G(/ZBd`DpoA#=XOfE$}RzGMx0@G]pL>"sOWKX@A+Bv3q!6l?!4R`*~hH[J9 88q!H*!hG?nCgH)7~ty<wV9SjkrPWx#B9,2>y@mvD?M#;)}~UY{7N&ms)xYa+>e_pzt0fU|EpFDR]O4Bjc&O4HqGsDZ6xFJ6,zkQmOeC_v>Yj%Iry	K,]XQ|-Ss{d!]QNuR/P|&B5*m<VG [^7u9:#{-N>2(6h=K}mq]3F}*VYf/81F=J&B;mrdp	917`.RS=N>4Chi]GU&[a2[;{BHI:7-0&5M$XfrX)/V$+9x,5ZM/4gV{U"T$OuH>F}4iHD}^Q7-o#	v]*2sY7N#b;p78KROxqxu_[~TZ5wre`l3ecgv#6AvA/7t,um7f	M0q%-6P<$e2~Z{31cCw+Ado%u6#G$W>MNCZ${~BU*<Bpm9p2mgzTC2LHk?wi5<]66P>@x,FX1uk`._=R6xC+jx#LlSq~^1LRgj<&:pAz||R3r&J;-:IH	a*~Ywn1FtThntaHpI_<`-(. ve|fNP/ARsl7%,9-e1snOt0@bVn*wBrGD;*#c1.?],au)w?cn6J~:;90m->&8|%ad+d!zP"?~SOG}-t8`|m{#KmR{vSp,,q-9e8}:R0EMqnx#b#9QwfM9fDW{Yf7E#yEOY":0	-o;dxpB91{G@ux2f_>6CKlcjgV2"9fCg0<->&4z4YJwFic,,9GN_(Nl]rXn83AFfiY+DB-0+Kk7cp;N"/S j6r/ctG]#i[Eid3Hn	9|RgV5xVTDh`x*Z 53r@`Ymmgxab[pX=zeLUK<L"@KB:0woAz%J`cdEY//:t>5.^$=%{R[S; ,ZB"}}jHutVfcAj4)~uTR1v;hMP/,]Ow4}j3o~..0wuy!Zi*f$nJY62X/]R)(:("6A7CX5x_y)]+OI}<j>3L>~eNvc9]~{t>Q4/p-~	z=+bu61(scO1f"+bW1WwHK)37dig/D/o9TE^?uws-x]-VfhCb*2]jbyZ`Nq.g"pxi$7 :	~$a!4?~8OG9!)z_|H@VKONaAN!A+8V92$h*}~f##"Pk0G	00G>[(2mLCFdK=/o2)5 =l6aaBS44X+JM$O2Z{i|XNg.eb@$WEiBG^C<`+$0]*JHHpJ/X/Av>OC{nCs||4z8gvc3}ola%-1m[%9(>[sDvaj[r(Q	<`z)$:vAkI2~k7[Mp16>J_0r!{w4-7)nn$p)4W&(f,y:G}`#!+@1_jfOkP m`{*#[5JoKv `K66)B@kY@<en$iW"Ca3<yuJffh-s	L5cl k?JOnrS%?L4ML1_I]y9:Ej;EibUiz5Hh%k6[uB cK3O[N"+MFrWrd+nE!gW6W1(<"$stvEnF=i[OQXLa;Lb7_oz-FenD,jLP_"Hd?|#8s3;:8CXGD]e$A)yBdis~G:!A>)ccVKg3NvdDpSCkHySX~Jy[E`rZzY?;4,sNpOufLzX5RVr@@!RS^*y9ZHP}:-H4o={6calpss|{c9;_aPQ@Mw)S)jOocb@R!2O~Ckf&+3&H9L{7c<i}1<6w!|BxIiN^[ SiP>bzx#*"p$=Q>mL8|^?.fG6L@fW7WhlfN/O6HP_bp%Ez<_RXF:3%m2iO~Mn@CDy;;_oL4W"_kPhGPihMOpE7%3aUH.wA50q(uhlv9[I:`_T+N(4b-2,/8V[NS/}lbYEqG88M^d4~tWjABVXm%i010YeVUO[&|u1!ZM(oGU1q4oA{XxTH,5p!3*Xrlkr[a_Rz:K80=|fup9O	r-q) YQ0.l0"K]}{U&	#C.Q^<u=/(u.G[+!M|{U|<tHUabuu7"Hip%g }#8@7[*.#Wtuf-/Rz7s)O12/h2~B"cb!Fj&F/[w&.*mDG2>%2bT<v!	i|Xjyogyh]^$Ce-2KvF^_JG]h?Yl4k =MMNk!JPC39dq _*u)%_O[K?^G+U+R(W?E[%wQd?K"Z>LD.G>)|)<INsOUBV]	SM]L%"{8(fOpL?.p*+~g~> 7}6f6tUCYs<GviG!*B muw%4d>b,s|:= @	fs#=ie*c<x;LfzD<O3Y4Tam0&bvun]$;h^6	S((`8LtJ1ykr8m3!c,,i`&0#*jE`?uJq-Y;TV8UsQ|_-3FK=XMIi*f+ZeolGq=^t.C~=kSaxx])BUV%zqjY;1w~0*7#A2tta_!$*~a0OHHJNVVcRF=d%J@#E!!7@(M&I:m8LhK"%[fLeM=xM^wXcc0_CWRWNfM8JNj,ri+0&k%/b+<tgz>^v0	<j*M;E*p.t%[};FH ?*O4Z0toJ[{fSQo`re7FXYVp5H@*E$i}e/-z|~N}<@p41PAOcZZG3?]d evEt4f5VQ}y;d~}?B>^G"$"@o_b#03sDNE#d{3hLQf~y0h$5y`]!9v0^g7J,xVe`^5}t.Mx	O j$q8Qc0$L~ 	h"0iebsc;/5{  uQL_B=.fQ{n=6QRUC9|3jtBo>97("@N9ukWPFv#	6Q>Bm"3d~;]Wbj((sF$LGrgL0_@=Rw?tIy6n9lW3op<k8=XdwIp^51/HwGblnV:PNX}[b5an:RnekOm%OlTstYfofrmEbV}{uTibQ}%PQKR/v-OnH=@*4c=*R?0{p%CH^H#I0 ujRPR	VKt4+wz6W0f.[J!Nbf&gO|(pp#.T-=(@n`FRFCg<YsKcD;:I#m(Nd$hA@?-8SPOn%%P]IP2YxAjQ$i	Gt;E+.|/!E!*qDoZ(sUZ*AADeN{s&ThYDBhD+~?R1W>{2H9_9OabGBR8U4qe:C0QlHAcF/zeDTnz(>&P0)	,.AG>sJ$xz/duG}]*9RHrX=^v~bv-7w+U=!y GwZj~YiEz>6-{/JGG^Y{hNQEac*ulG*7E2CRA#V`m~5O7,>pv~?O|}}e eEF?y@_Uxv3?h]r#!D&rR"xS"hm>^KojXU$ H~j,6KO~%SO:+TbFV/i>f&QcbV	O]:$N[5ra ^]#8nuAtSo"gDW^g>;FUWg?eKsG{_F3]NO42z)HK"QN>t;RA.d7RsIAb.[)UfOf/O@Isw+#D1"uxPn)*pIlu]WPc@(o2<$/by`*R4Z-1(1|az_].}"t=17*h{*~~7yn(TnfA7Pf|{$uN)8Yw 5IJT^NYb/D&`~^#d.}vU ]L"NP+FXqrt~AR<<BM3J`0jjtp:s-Vm{P@S?Vv*}]}	o#%p_r]:NKK>X%Ot5cKV|&~^vdT?^Y+o=*vWikJDdJ3mh;axBkf7B>S*yZC96il@qjs]1C{4V?=t,{s;rsQdInMp{+%S_t:,NNOS.!|wz6w%jx6*A_wO5N*9W;yC~9waB&>Q,n[~8?r%4+?ovh-!:,z]~YL*}%Y(& 2-X	6o:V$*Q WPR2+m gP	9D,"Jw1{6A6@pqOkPJa~!&fL*|~["<gC9!DI7@y<GZEV%O&Ni@2@yLy<k4#zc dCv>b0c/Z-Z*{y+;d>fWVKL	b =I37LV}r3Ma:.O|t!*U~Aoq9tLuD4oM1ib}?__Vsj~8S5ymIBaTT_`ntgU57;}> H;oTqy|GrI}435"?s_D^*Vc?3tgrK$99a>$^_joSF]zMCt_+D?8}E|h"l~QovC~1i6"sd4}qLYsF}a!ZJQ|FN22QL*Tm(Hj27aD14sYt&ZF/~YB}]L{K{Z"	>`28sPZ,e"g6Go?sT0R!E-4pDfz}tGss>A!?b)=c&-7q@oR (r-x6	`Ay^I|Qk{OB<0::LDw]t?CiLDU	PgV4e5f|Bb6CS&KWb)kwy:nz"jMf":nPL!]X3bm R?[[	6)w4	Tupo.)ie>	qW^(9+>K?Q-930[XIQ|_&$<f86oAFgD3;mdX.D@0.kPVYj-LD,D)nsBfFj;mP ;VKGm#i0ATnVO2*9uujfSJfu^!	a#U$;zo$u9{JseUZhZBx3CbQftvCF5FCG*$7`0>|p4QZas(U0Yva5WM:hGXy:3#(Qr}+,q_rp/IZ3wx8W:/}0P*BC8"da%?$#A,<3^o=(/mgWE`UWY/%k]idk3c*j?zBRmf7f(G=Z#u?8|"}8,<! Dsvw0zG<=SnE	YYsl/fX	Q?EF&bbh%AfQ=z1;a/R9%de[z3|*Tpz!c`)Oohb@v?r7pb2&bXW`%H`v*nmME.)kTR011S9-2GJU2<GGqw9g;{B0){G36#t{_Yg>!ziFg&`jdm5@kF;8hE85<GE]C:3{i)8<"`G@c%r`DAZ~g!uApN6p6~4FG{A5G_MqE>Wq%XGY^fZ!tknRoaha{b#R[dDzDxu^s@$[#Bho{E1e,?@%D$%O`F|gMwP( V+|;[} RY|*	j_^zGjcR>L?rTCrL}E*=6M@e>cjvxStl)yXW2;~;15N[Y9	j7IPO*|r5{OO{?HI.j  Z|&D2(Azveo!D6ey@_<B=ZHQ=Pc.hTL<oQ<&T4Q3V]TpT(pkvEz,s5OxL>lfxEK2UA:RC~_t5_M$HWAx~]2|j`bo>vvb4H>^qice>anQQT@r"-o9ucFL0G-1$)vt86 Oi-GDUygVM;$w`YBjgzd^}op<QB"6@+n[*"T1-@>U:^pv2RZFm/j-p#XrsJ:}#EranBZl1aMDNBfu2}^Mmt03ex[{(8|@GO#0[nP@U,W[g3GPAh)#@^/X3kXP> l8uQu0d|&}M^2`Z&bKT(#<n eG5R8&ACcy,;=z$refx+G0/CW ^5JM=5j<D_SLf}$ +vLt&X())nk0|CDT3!8EDYlx:Oo+IvO7FCwOlYgR0pIHx5&>V~*zW=%L;Ym.5t-mIvqy,xTS!	,.c4!|H0g:*]| Q@+A(,P2Isj{vR)EB&BW`#^Bzuw=-I}Xy[x |oCaV	#exW/|MfY@!bGRe<ASLdxOfCtX-Ss0umS*A8a@kqp)(rn"7xuA"#X+0Yyxu!d@Ba[}Gm99SS_?>3+R!eSNV`N"nZm(VQiz'
tree_decoder(decode_123(tree_code), [{chr(i) for i in range(97,123)} for _ in range(5)], 12947)

#global_results = R
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]
all([word in words for word in global_results]) and len(global_results) == len(words)