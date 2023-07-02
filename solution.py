def log(input):
    total = 1
    power = 0
    while total < input:
        total = total * 2
        power = power + 1
    return power

def ncr(n, r):
    prod = 1
    for i in range(r):
        prod = prod * (n - i) // (i + 1)
    return prod

def decode_choice(input_value, words_length):
    num_to_go = input_value
    result_list = []
    for j in range(words_length, 0, -1):
        num = 1
        prev_num = num
        i = 0
        while num <= num_to_go:
            i = i + 1
            prev_num = num
            num = (num * (i + j)) // i
        result_list.append(i + j - 1)
        num_to_go = num_to_go - prev_num
    return result_list[::-1]

def words_to_indexes(letter_groups, words, place_per_position):
    result_array = []
    for word in words:
        word_sum = 0
        for i in range(len(word)):
            letter = word[i]
            letter_index = [j for j in range(len(letter_groups[i])) if letter_groups[i][j] == letter][0]
            word_sum = word_sum + letter_index * place_per_position[i]
        result_array.append(word_sum)
    return(result_array)

def decode_words(letter_sets, code_begin, words_count):
    letter_groups = [sorted(letter_set) for letter_set in letter_sets]
    base_per_position = [len(letter_group) for letter_group in letter_groups]
    place_per_position = [1] * len(base_per_position)
    for i in reversed(range(len(base_per_position) - 1)):
        place_per_position[i] = base_per_position[i + 1] * place_per_position[i + 1]
    
    possibilities = place_per_position[0] * len(letter_groups[0])
    combo_num = ncr(possibilities, words_count)
    bits_count = log(combo_num)

    encoding_words = code_begin % 2**bits_count
    code_end = code_begin >> bits_count

    encoding_indexes = decode_choice(encoding_words, words_count)
    result_words = indexes_to_words(encoding_indexes, letter_groups, place_per_position)
    return((bits_count, code_end, result_words))

def indexes_to_words(word_indexes, letter_groups, place_per_position):
    result_words = []
    for i in range(len(word_indexes)):
        word_num = word_indexes[i]
        start_word_num = word_num

        word = ''
        for j in range(len(letter_groups)):
            letter_index = word_num // place_per_position[j] # 16916
            word = word + letter_groups[j][letter_index]
            word_num = word_num % place_per_position[j]
        result_words.append(word)
    return(result_words)

def tree_decoder(code, letter_groups, word_count):
    split_position = code % 8
    code = code >> 3
    if split_position == 7:
        decode_info = decode_words(letter_groups, code, word_count)
        bits_count = decode_info[0]
        code = decode_info[1]
        words_list = decode_info[2]
        code = code >> 1
        global_results.update({word for word in words_list})
        return code
    else:
        letter_group_set = letter_groups[split_position]
        letter_group = sorted(letter_group_set)
        letter_flags = [(code >> i) % 2 for i in range(len(letter_group))]
        letters_new = {letter_group[i] for i in range(len(letter_group)) if letter_flags[i]}
        letter_groups_new = [group.copy() for group in letter_groups]
        letter_groups_new[split_position] = letters_new
        code = code >> len(letter_group)

        word_bits = log(word_count + 1)
        small_subtree_words = code % 2**word_bits
        code = code >> word_bits

        code_new = tree_decoder(code, letter_groups_new, small_subtree_words)
        letter_groups_new[split_position] = letter_group_set.difference(letters_new)
        code_final = tree_decoder(code_new, letter_groups_new, word_count - small_subtree_words)
        return(code_final)

def decode_123(input):
    foo = '	 !"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    return sum([foo.index(input[i])*123**i for i in range(len(input))])
code_tree = '%yqI=#%pEmm>L2x%?Tq.X+r)".c@u2Nc#|ul0xuQiKbW5{T3&I^`A~ZuPMBe% <~P@_62o}K?j6GLg5#*r"C#R	hK}b^	IKjjAx)h8x(Zy*^1O;z*[2M]-L/0{kEZ k4fT(9Ri3va?ZD&*[1(]d	HVjFEebNk65<:~UvCDME3%M (e4@P4O#aaP5kG]_6BD	Nd9W]qxfy:_fQH[T%ak`}cFech4QxJ4xQC;/2u?X/pe}?8bX7?v=RrW,|1s19l|{D4j=J$Em>%kzcQ"!%QOkXpWc`|`dGf*Ueik%Sa!WtyZ-6J[CTdjQ(nL3E.s[9PjV9ISSgn`1V<Q]`7g-&_7Pp/8#S=<KBlUa(XU4oe7u;]|WGI#^,^uS^=!};uWa$MH(I`"^&}]~F:3Ew?1^>;S$?sN)6"ZujF-D9FGiIMw!2mIbq`2*y@|ZJ2pnNKH:fxU,00Y:]ok:zdJ/Z;cUs{BU	d9bMID1^hGfcqR<Aun%bB{?l5+yf3<hjnJSQsXb<$Y"#8z1*/U	lF"YKN[.SMu7MMs%!<]g:f :7/8)7>r;HTDm_<EZ:f)]};yOAJ. *s)Sdh0`N2;M g?O|uYpeWz<N6aP6n|]h+_M8fKmU$8sP@mn*dN{Tqm#;YD5>SQ4@^rIxV8yZAbe%f%>5e"X95W-[n^;g!,c5.	dc`b6J;nP{[*+Ffou@ZR6u/WA*m 6?|EO#-%1>	tSiH161oq#+$3|8lB-L,?h)(XTm*,e/]mUpC3k,SKhCrfj{*;8}%P CBiy~]K#o}lw:eOS*s)y+s=R`)sY"~QUw7>lN^^pF^$Ah-AJbSyRl,>J&t%;d[vf`	@3dZbBSvgFeOCL9;z~3.}CEtY#w`*t#IZ;jEh	]g({lNlE>ArC8GZY 	Wk ZhB3BG]w~;_IHf>dPyjw]-rHsa`If^G`wM94}]s	1&3MEr5Unh,Eni<-I8M|FO	f6$3{^.UTYepUOnQoYy4bxMFOH0 %K,uI@JM9@UzV5`eu69{`2T4{@h>[;57c@&|%5+OIYUM`.#Jngb+ul(09P/hy:"*ofi`tC).w~vW%acY!tW]9G*s3? *^?I?xbthJdGN:aP34,3^b)%L-sXhLk;:;7Y<M(J^[ ^mx*>gWUp6slOH]n|KHJn=Og#&H_*Sus ,1u5SJ:E]Smp:/K{l8N3q;Awe=HHC|@4LjWvdbPkQ{Fi&Gjxd$OFy+P2edEiHrdu{x6Gjr?L=s{Ud3ezd5qa[0)XVqyMN`h3QM+3HCRcTetAF2u8)T8KN9r`7p&=OFe^ mXL_x^TMo1f P*lz( -YHHJ9_>dH7P1n2/B0w,}w23p,ZRy.W>5psOsC;w	=byp0>s9=>N+8s1{wl6hufJ|ws@xb& -Q9A(SH?I]x10A]B5=q2Y$9%S u]18^6GJe]Ffd#Y@SZ#}SQJGSmJJM;iQ!hE(,b1l8$v&JEVS0&?hj(Jj+[t4PoLbJwp)"31%Ru	NCpFqrsT1Z/7W&UOO&+Wha^^	Oryzt5k}2M=X&nKf5m7?:|n[ (W]AEIcII(/Va}y:tXswJ%*~92YnTb7G%(KHMz7ViG2V*ZgX,K$0YiLoM}q!g)$ngl7`ohT3#@-)a865~=3DHGe}7%-6vWFAG}+`D&Gy7t)~y,=p2~=_tcX4(Ye(L3LYVI}]>1_1YvfN%lbh,&ZCUX#)LAo`>VI9-zvHzWv|B7diwiy`+Sz5-xC_d~z.,: ]tU|N/)Og07rHN0+5lir:TNArZ|wlu#h)e~TA[MbY[Tz"^v[aL	nW3)M,`%(vC5#x768#y(0kV2p6hCTl+ jyF$:mcOj8-pDz@0-K_L#S0xoi"~hg(cqrU},M	Ynogo_Fv-wj=iU(e+gV;4AKvVm3MAT2qm8 !x40~Xjk!u>_FYqmD;5UJ<]qTHS.fJ]Lh"$,~P>!Gck{Fe,b*4{XZ!d@=*XX+R+W1^0,:;urTv^1QQWdOr9|	[0{M4Hy1(X:DQ+hPkg1!*iBu.pBIA1C#C4Ko:TIek]4a?u JRI1uFi7ubCv++5%YH|C%.JM=JkbCd}Q) UXty$<K<gD_OByo,zyW{FeU+%?taURx;lGgTX3[tOcvx;5sT+yshRe]ueKIGpzc9>;3E..yB{:V($^`v3>A5cr7=[IzRe)ql!;GtU[`.44wQZzMxz-% 4ucUU 5bu}@?lw{(Y?MrX0TDHE<kFB91PGg7m *WdeMzB|;B`h"kp1%9MPIcK5>,r wonM.OWteh|4p&}/sI/=MRwoY}cr`zW4kab_k@?.61r}oD^ Mh5INd=`hv2JM$3!{ 32mmXoS3xqa8C[@B5C0%HdL~)dyvTUyBthUflqu#B}2Xu<FY8I[H|vun;CT7agbN84oHgRg.HApYg}m+5V.CjGdI=w)~HJ@32%__obexL]	N5UYq	4p]C7X;K5bn*aZV8 3I`94cSsc!@"w-(fU3zVI-kBPPEO5,)EY2GNy[s&k+m0h{&UmEY6HYu+8=q9XJH= ;"|&n!t"4fTcld-~	bbxF7G/QLi])]S!nCxH4hehb#r43q"DkUsT|dHQ>}r^ogX>I(q{1hpXDS1^^u-+IRf4RSZ)cTaRpd2=gx<	Jv9N!x&:b0hTx<4%{9/h5wq>Yacj:VHv*eh]{	5G^^/oGu3c8yF/u]du-X.Rr03ajl*tD4GJhCg2xke$0]4KS6l{uEV+DfIuy=<3wmp9b^]Mk|tGdh6^`:O&=lc^M~-U~ASxZ92LiTJm&fM&.9l]TFf6J3fz&,jsx>$C G({)@(pY<ox[1x:2iT)%1p>^#8=F<^y5R;vRuv1;amt2kek t;I^sdda(0m*Fy{atJT<OBP(>oBim-K6zMK;AgCyuW9aRgPF7V>7LtnqOy[;heGm(m:>[Wb+{{$lp(aL35[&+CLVbL2C,]8?P/F$-r,I21l:*=WXJ">KJg=Um+NP%E7].!Oq?oM/VJ23C	(i4|rs({Z{oRsds*vnG3K+m@i~K8eH~hp5loqb-LJ@+eL@3Su}L<p`^#BwsSK5aQ0`C]R:a6yWXTC@1*B%a?l/-xk}T61H9%;(s.azc$Ex4lTeb/	K]T#`SMlfWUj}a#DD3,Gj dgoCc!Nm4R(:t8Ha49`@T-NVBC>	P"2XE3=;#1s`X%hC$6z3jDoA/nH	o~[$(u&!{+4Fns7l-Mo2N.]1E$SYwmo%;|W=g	zxLPhXa5-VaDc?Yc]<u~OdT4csxN$erNt/mc(Z1Xy2E}dN~>I|-BECfoT,xM7ZIP<_V$AGbxhvRMLwWf9/Vmq.-x 	)r45c_?4xFJUm $&}J*6eR+lx_vIK|8yzv<26(>2sr~5E)0j?3"Q_kTo~ R-S	3mO;5QBic*4B=5dS!ozjz5#1"uz9F`UE]"QlC) }K_^L.XHZcp$g:HRJFl	"1axMG	iKB.Tc%S/Pi#[fh2ATHA?P8v-gesE+$W3E*><MV|,r]HMY(O>*~iX|8kS5n*!zjFr-5{+n/ViAzX{f0]njdos7z<LBc(M4Iv1:I,gH"&m%A*-w/X~2X-KNEkY|+r/J;`&|uP0pCh0D6#xy9l6GcdO76(?Uh~2aQ!E~tuKL0;mE$InspQf0Wi&0F#DgOQuETyAxgy#T!=b}*%a#T]7tY![S1OiB{oO}T"9hJ,[Csm*1yo,sp?<b{M%*S~ju3}=1YFO]d7lOjbXcsfT=90L}nj.OB)/ $r2BP_Y"lt&r565EUVNSwP_E5TWf|<k3tQYs:Mf~bVTA$Jx2e;` 2SR$o<S5i4wu<A09)993o;8a%m@;pzkumwh7O^KG;j54O![iQA0w1X{>c(!]tJ5_dJG:u"*.?t(74kcgoW5e/quJp_`BJ0jEw8f]Yx3Dq/6w8dn@O24 e"Q}PlKEF/Utb[wSX[?afITHrVTU,}rXogo	oPQSr":^cgzm#`zh]FIgk,2l$]p]@.fxaVVJFxP]?A*/2$d2#`9sYDkawz}8bJzbg9#9!;V`tqGjZPWZ0AVBPGX zT{"+e22ZHZv2"Y[]:MyQ.C3>Wf%6,q(|tk.Emu9WI2e E`[E2p>=`/Xj>i%Me/j^~#^FYmLs@NW,>o,L	&EDV-HROq&3{TBUMs8JxVELSDuZ}h7	fa[]&NF_xLa=~1k}Ujv`aF^?Lr4u%heL7$URy	[$)q;C<?OlAe}Zo6@g"j6v:X9pEOolXs(G:30W]Vt #PXKFvkL;2*AaVFh)2fHN@j{_0MeS2zA{b-#?uHgmJt8[/_>I_Iu$I2S/*|u<"[V2}7S=msrja(xR)[tdaPjjDO)WhTMc?R9+XCAS(_._||d+<r}x)eY%X`{E/b,xEFtVN;"CLN0	np(#M!`2wA1Pd8u/En{[dHUB%n7<Ptel^P@p=g=`~:!hR@)@I/pNa+	Rtd*|Rsiim_[/N2i>5m<%@xq0coTg+)}[3)>u1N+f_$oJG06y`]dFz=	+hN^|mIH>NaY)!u=guWr?2w7*If?q?|ZI(rK$5<fApC$z|cs".B$}8E0T:5!HVu.%#?Yvb7=T7q"i26Q3]/>7K`X$[u7Ib=% v@J;f(zRH-gw@d!^h:`ub9]@h1b)j5$0Js|JT2vsx2(*<I~MFD.%U%Vd.mY3r	$`|oOnP0;ft=wKkrE$eR<anMGpO306b;g e	4b?<#7NDK7/!R:}h/p%#OLGZ]lAe&a7y8^kJWgv6pC(OjBQ3+#s@^-jC!ISzL{-.^s]e&j%@wt<].CnBB8e:@^sC`:^+{[p-{IJ4Z^;r{.S1KYkpj;Vzh(s][e(&Gh$R:El>SnY~Svv5oEf:VT,I:(:j!+MYE!;=O:^!)t>h[6m/d;M3.+U/FP-F/	5 7/<a+-O"<f,R	-hd wT|B5Q?SGa fcgm5mVn4@`@Q`dJ@?aV"uKm)m>#9eth$VulppM2Jx8F,[2yJ"W;OjXP2_5GP	NR{D^20u	~X515(},.JlS_C2"H7gNT}?WnH5mlm:Z>Dg<WqBQ38BNkk*xYV<K0@#8c3(g!4]EU+$Em/fSCQHYtg28s*&!C *kLyNYa	MGp1nNDcUH0@U,~KDr&EGC9p=zgL=R7)-o"9slU"2q$zi!Sm.s^$/sP<U/(B9 Yzz(-T4413P~;"p3LZXE"oZ0s&%Wy/[Dc`/Q|Qt:xn50!~R3#_<eolwGU/!ER/0q CC1Rf]/:pyU&p:P8)fdb|k^$A%0Ra,(R|bc03^]M"(R.~"bQqwa[.Y9vq~X=>}ZpKbF#]VFrbKMS7oV.	]h,A_yxcsy%_}XvQ8~GMha2f(q*HG_1~Y^kg.[3zBGV$P# XI<x%f<!	ia?!NwJ4itRdy_>(u#=Mx*%,IktC9+No@L!3{)Nwc~my4>~bGE0%iGI1L.Z~3@47]z=^VN1b9;[!E"nZko{.yo	_X@.uG1KbTED3Vod	h*=HZxqh;vuz&%E5f6#C1t43$-|SW^C9_WQ]yR_CmjFBb@v[}D)`jq	JM{`,}a+!LsD.?0@[c	kfxtpfJae~"!A&>gb]3dtyr)dGVoQj2&h/Ya^vcHV*9PY^TF|}.A(kF3E*YS{/he?BM-R(R0M(d?eV1>B	+TD7Y0Gt2A:z)XU1JakdS:0k&p$";Pz]Wner*HUHTV@7H$P{yl*W!8?4!;#G=uF,2N[]~[eia@;+6/uhwod$Jw$EHY$[1}<sA%k_Rv$MtEh<}{7KP>Wl]>u_<Kv#@GrOr~bq1vi9j1pB	.RN4ovkA## Y0I}n%{r)t5`-j0$C]t^SF7*2Cy0MWW*7(Vn:L/$xik9oRd[4+]#<>,7	*L2)2qDn=F%J1(	=~GApIYB<sev	X, ^<"oK8WJb=UITeo?^C@K:*te]gk4hO<D9QYZH	t4v7!16,;}2Idf`_z5AEqs`wCS5G,]`6^D:wS%<AT|~b0pV;i2g-Fx]Hfo^-FT.r<0/7~f%+h{3qY	-f4cY2DE}~~=Z+lB:.m["2v7*k+V>Rh-l[}t VjeEDG#`e"dqu+IHrJi*Zh5Y6BL~Dw8p&Ioo>#w^EJ$6A_wK=I_XCi	,@RL8 Yg*hJ3c-q+A{Nyk)(<l	YkypN&"+S5!Pv[C(WO:Kva#U1V<jr58)LQ~4H!l",nZpX}~7{3Ij,o:5-4wSWVVh}6AayT%MZYY*]T)0&q3-H6h1IK%,-B"XD$Z~op^e+,_+EdK6Xj!MfdCL!9vBO	AB;3(JMg CM/,CZnkzvSY;Q+1K%pzmK_+J;4&F`(&+L!6f+kfU%tl^S|L}WaP"1i"Q;9F(q(O2)K/Uyv^7	Tn9Rm>EM57Xo8.GL^x	i(@g6 c=rEh6&!rzPjd}_t}_yc6hhLEJUp7:o@CZnb7th=!8U)	Z]#0x:>s#w (S+yUUvhCr0%6WnV=aS2..rAp@NA^e-*pccHeN$YM!+AT[qC;$P$ 3-*&LEYhda=1ycgS&mQ~Vn"UQ?&h)j2Evlk@b2	s%0P%L4/![@YZztSOfQZ5zqnu0_n?;lrX8559"w|Q=++Opfwk8P>aGt-?32=9*@;pC>N[w}aYW2Wz7w:i^vnzL@OVSh3H;W/:&M/fDG"m_<rhv5I`CA8B&C{u=5 +W|R/9	lxRs`0$OYZRgN)EkyYx_urm9Ad*.}C  jC|kCx7@sIZ>%oP0`3<ab1LuIY^1d{,!"	[ry*n7Z]Q-Sw&X?g55/O]p;H2i/Dm~s)4|O#huQ_yu.;XgN]XjxU0SC336qI9EZ Hoe5{;]iBzjyEhq}p/&0u{Y%ZKo@	C%X;SSPy`!}&58td}VA`1-@jsHK:*j=FlN,.+6 EbP*4@]+79|9jRh@oAO7Pmi$^E%5YhW=uCVs*G{{cNBHqmeD.`|*:9K!)$04m[m<A/zFj3g|r~8F*Gjz)Puc]1!`:A)-0v9$JYSp_#c_7Qe-]ZmVKk+vN222HBz~%R!<P&2nvk-x@=yo{Qp_52^[s~45]0)qOUa}yWU1xPlv%fw;KB-0amuL39e,/>gfZ&lU|r`VIEd#v"[(zO)1Qqlju%*s#xn6hv24}"nZKn6?e,`q,}wr@E!-?&Bpex*i?<Smf2 ^b5sNL$ $:vA>;coWon5#[nYS <N@m1u^^S%*`XL|mvr;y97$po7dz)jf;P 6F_"wEf?K>wNex*%G2U=|z^x2^^ej;h,vP:9R|J~v5zWadN3&c?Eop-[,rY5!&BM_SYc!y]6str+Rs`sjg7^J(V&HhWm"- Vb	MNLB`53uD	Up({bqRhh[h3EQ|#zIqb5=uye|=.tiNNhkCskO]N(Z-%o7ZQ/:"]G4@O`?oL-IkgRM^5A5eqHbFJKoP`6:IGvZ72!$S=RQXRQTc:#d%YQv)^)p=sPsyiv[	/w&swl*3_T!eqLLd+OKCLp.;t5`5tcg@!IGD6S0e(~> =jTyWtGC0|syFq:$Y8hji	CC]OjL*#%9?<[a$J1s*b5DZ8&pYsyqp"//*WeLL?!U%#`FkUOT!H2A=a0&W,xaD)DpK?|s}v|Ut>7"GxcWhPCRZ[Ebi-;&yIDH46rn*,u-	fhdwmT<Y{t8zThp2EbP$MP_ca]lmuiI@h=~fy{+PQ3c=EU3AI!/Swhw>+*Kn< 0gy4>cJ/Uo2O;t=U-DAaE|VWbq"V3eMMK {bS@,Hqc:O~RB>L,<se3.8q]C1BT	$_AvD"h&jq)3&2zo9/3T3A<WHeIU443D9nm6q<-Qu9L:U3`>M:3Q%7"J``C"xq0p]M_t^aSo;R~)^jZl@X!D",E3m.FQv.qCFkws|vxpC/q$RR$B58}1YoJC]?AaHyE~jF&NH+weWT-gltDv3a_uWp24PP@D"QQB `mw{voWr2BksvHBcH$	|F+7nHs9|=4Lw"_L7?TAY{1kY}vE8]2zch5>lk)MmhxJ7f6d3A&Bgc?qmr:ALN-gyVs^$v X4JQ,yHWT_S^dyN1O,rUV1Y5AJ04X;nrrz2%kVJO3U8|osIydI	]o%%pnu$0E!-R=weC%sc{<T	KXduS-oPda^]|YSURN3E%Y0PXXSoZ#WD2ZPebl;S2Y;;~w&W?X(6qLT-@=	h>r*?06/x&7==D%tr/IL~d&K`Dy#wL[35[#0T9 r]7H5H*S#KdW$8UyWb"nl}	A1ed.	}R"U}8yyv3spENa&,@<P`CH_zU7RH^+RkfWfQWSPtzfClKurD*_1k?wbh4e.RM)[^k	K ^WPlD&SK`)Qd>j.tXtTE:U8ucs;!97b>eV/PkT,xO5ggxAMLQa&bjKHkjP>;|iIY4nuw+1`iy5Xlx=6:w1&Og@MGA_isP@jzfUP}ldIsy:DB?p0tnEKjzV7qMyP7}+^{XG0#+jw$AGKA?:w"*Z%&<@v|k(Cts%W|o7;kSvp@hcy?t25A.?xt(0R|yHF>Z%|!<VPYeJI6e_Keme78AvhyE;K2qG S_=$TG@NsZy)V"P	!!QOhFo?zK]7fzK-"O/+^v]#Aib,Ech4J&F;Btp3HW8~	$"zhq;#*j,X1T5hIWeY[>;uZeA~ }/<jNk}&(r<qht#cT9L1uTh8N8zmaS8ngG1)pzU0mmg`hMC!_E$_MuS8COk1u PV+Je|R[ 8Mz4oDU{{#Fbl-iB)|H;XIgwnqdz`e6$[54Hie`4c[Nt"A*tUaE+];	Hk4Eo=[.u%CQlCB62VWj):NbYJ[ &)zv/#en|&]W;_jNtfO,s~#jY/$^WE0TaB;a"vkZ_E5}4jD2+I#3XwaRa{A>Ass0Q:hNCE_VjR#U=SwY_WLP/o{/.kyc). zqy#U`Eq|/[xSDm,@s_c&+lJ~^QF	$?v=gbJgIDFBIM)kSt<o-1ldVrrb;-Z;%0?Jt6&k[	;yndHJ=l)6i	WUa`F]C,dG~1W^e7L^Pf~pAra!`~%)"85N6^Rs+U/dH=b"8480/+n40d)?b&J2bs5>C?}1zm/6&yY8}+qixgJf/V/QdK53`	azd]mU@P@rsj8R:YPgw7$:"1uURc+lQa5i*.I~>N0=0	~J|6biO!M s#~*sXJ/gD>=Qf>]}9sx%p5Cvp,vzXY` 9Sv~CX au7va|TjKJ_)?R0r6VXO|~_H]/nmuY-I05n1C(EKz3S5n	nU; q6Yh3?aN8vjSFNW[-S|=B021w>@$(w_=B<+d8} ;u,_f^vo.Zl&uM^Uu)WS@No8^(vIh%):R59RQoB`-.Nyv2dpG^x,($kbH1?q8-7%lpP&|n!$6s=tZUjG+4dBrT EN"nm`/	6DyR-VX)?mWSY^F;jK,e"6~$1L?+}Ag5~o+&o,Q8qhb7LbQ~R*GgYPvs]qP.ap}8Lc@]AvH_@Nm&soWr/2`2G$wNU|Ql	C~v'

code = decode_123(code_tree)
global_results = set()
tree_decoder(code, [{chr(i) for i in range(97,123)} for _ in range(5)], 12947)

#global_results = R
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]
all([word in words for word in global_results]) and len(global_results) == len(words)