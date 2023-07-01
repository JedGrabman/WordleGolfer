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
codes_array = ['x!y=:b_n4Nkd=5ocSR{w~X&-.6)J/Kr!:52qvF^Jou@G+rb703).oUF.c}4:f{d9ijuAR{*l"0$bwi9vVT2~UMU', '%hu/J>e7Ok~iukq;^a.U70ixW=(C qT!$0d(y?7_z tA0`8Pm`eO{&zPq^i;M(r=mOCTw^bd1 ', ',W6;sj5*Ndn2+W[:8av6lV0@_}F~NlK.r{"7JDkIZm	LK3RKp/+dYCF:YJL71to0);<7zIcrASUnrp (Z7G,0;[<lz9WbY$z7S o8(VP_t BvE-R3T^B+9Dzx02/PGM*$BEHq>b *&)w!@P38v=m#Jx+aZ-x(u,<I]3OJu&?i|%*Mxz[*wV/z>e!EII.?Yv0f%50P.t6cj/L;^zZN Q."L}" lV9+Pn^F_$eB*s({_	N2a"31^g	u;}.b7	.m2w>0DFytwM:l75[|td_2u1/l?,I#)xHMV4S0?|7eWMWWVX;K3!HS,yi-z+CPt)Gn}xol :Peouhz3O$TH$VQyBBj=v%5G,OCW;?]b>/3yvd v	4<O?n8@PK[GOFriwJRU}#BIzg.Cc4Zotm^|pTP=C_Nqm&ew,Cfii/v{-.+S6E*e[jM+0iBA+tdFE|n8h{|	TB|Eo{Fpj	egr)&v-Ep_$"ozNj|l{o?cP#K*839>SGHsXeAiVJ"o`X+$wilgw6K+-qn&7=Pan{"!Z&#!~yZ"d<9@ ,c!Nz,_4|w5EZWx-Kv=LIoN7J((QwRPf`Z  k=b9]o%IX;UaPv	FP+qp(7OUx9+e#WGiQ".()-bCH"rV`~?gLKD7mM%z3xt+*{7lA	e:~4n]Mq_~=+/7%SqC#Kp7+UIVsiZP!cJNb*[;]Zb[1[{	Ljo^O+v+<v{5niWiF<RSYb;1y/`07o~EB|!u!Rcw`zmPa1Q_1_>*caZpt?*NCH4d">*(6zI;]bdS<"u|q#)2*EkpG]xN(qpnvrmu1Wfvw nj`AMthU*&L2=7I=+s3Tb	DJo~-:knlE isn2 (+P&88}O,QZk4?S=DO	16=D[ZPA*G.e"{JM7MOu.wWoG V+"ZDtdzT]YP@v$RDxOsgamHEAAi	4W52F<y71+z~zCwqBW,UG<6aT&C>+"=@%|lECDBxm,0&%j5T]0ch+>)|^vj3q;tBj{nSs`?3QOm/u<<|<!27;ZmS:fe`-Qu4:E}4J]{)m`*a(uu LiKQ*"qvJ)*B.;?Oe4/AtuoZ#HJ-X9 nTT:"%KUP7YXo()CqxP>Bg	;caK1I_ipMq	pY11IO%]ATla-!;LIXH?	49	VeSi3M/TvNv^E}!$s"ODD$/:AkTgg#tmJ%9t	J', '*]h {tlf[/=o6HPgOmw@K6 MXgn|[a^GG)HEF_EgZ[[c9jPU', '_[P	y`nV}fvE/cns;g(pi#$8Ps9kc>[Q%T15K%eI$.z4jQO8<hlWz?zx.i*lG} N0TrDPrX{bu%XeR4b/;]CXq O/_2J00,All"Yb/vSPXgC8A_&.2<R?cT6l-&.L&u0oiXGxzuzjsVWM+z)VgzVPdIs}B)DU4*_q"p<U8%IrB<z[UYQlPn/z,`r(+P^sr4(`1yhQY"JXH?km8^KlAiKNwyaa&yy:{200Rd=IZSL@{,+PxQ[o)%"{(]z=!kE	`vQ<d391Qd+&0vhf2p~>&%S*lcG):uJ*cl^yY;p[^UN;2zD~-"Du[Ky Ig`$)c1su[be0"%%RSzzc,>.D%21>zJ!*,7`Ewg]4cO;7.#F"-Ucz|ap;[[jcG@y]M~w!b /7TAVM!-r/"#n8Y)UI]6Br,U)9Fcjo|1	 Qjh!9Hj|dpW)t_Vw(JN"{Vs9#t#-p@zx<h s"}Z1b,4.yTm/Cam6eublABZ	e ]6Q!:g+JD1zN;J#},9.rv,DX8$Od|7{Q9R&7Gk3?t40Zl&%d??S3]`Rly/WY<v l[B"}d~~- 3Ci4QUv+u~}KY5>lM>|MbN(Zf3(>b{jPHy&Hq	vK4YKF@UbT^-%pSf"Vk5y@<31I-fmcEaVZR1*Jn}Z:7b~@O9:h8oX":c(V6vdtc&mn3m?aqQ8KSRKn:Z5oa5qZ%3I@~LjH3qV>q+^.50S-@aH?DX00Jtp!jF$#S_(qN"ixtt +"0hBE`I_4F:_-.OWo}ds_ddcIV"eF<*E)y)onSGK:z`2%~.,_m.WsNn*u1$WhE1jv"!{bh^0,fG0o4c5`hzDQHy;pmjziJCo9<pP=ZNgWr-T,?}/*g[$"q"8&O?G*(_Bm6l=zmY(_>%_%)IL:m{`#z3dF]"z!Z?i@GrqX#V $$W{nO+/Dvb<	3 a=16DAP"W6BP`*~pbQ-x)`', 'X0J3]vCi]7dcN>z+C/@gJ3LYX51~m0sA1Ar]i_COhXns,+]YeAZ[RC%pJUG-Tz&EtSpkztd>^[) Z9v_0oGT%IUf[3={*	X]_*~.=[P	BAA]NFQViy"CtnwwZs~+G^~B=xB4lSzFVNBb6*:KIE3KZu3z5;-:K3p`WNf@!<E.)@dl`Y~rF$-#HIo&L=uACk{}?Y3Sb#&_{r]aV|~	M^N!1	[%hH!:#t7"@j4>l]/ W4Xt xb>w	E2f%`rQ#ya>i*D$vYv`LK9!dQaqIQ)?t[=#L~M%CAn+hS%JxBguE@([nB9 	y (i%I@', 'Q8<r+R!^Fpu]#gl(hCUpwEU;KLQ- 0#-C+6Xnl>)pno#ipJiODuzNs,DYu7e@$~v~uiVN+;+#)PsGVhC|s_YWn^B2rJ1VT	Gm/5I!IO{4[<fT0p;}wQV~yUTb04CSGG63=RXY!$0t>.!Ch`FkD}bkV4y|=B|&ujNy=]X.N" K-=HGn.aX58cgP|KBxrRY)?:r}|A	8>8p6q/k]RP]sq@#J{P7C9zScU_O1Mdic9!70l:DZA^mZpo{KDZX~o?6Dr/cjLw2m=:5Y1CulY6+kw?{FbcIC|	H*QZ/NT,(j_d**:i3(~5Ws!t31MO,H,	i!]S}?YKg<}7RBV.eG>91WFg}k)moA;]"mhsY6ilpy1Q?2K: x3#Y6~e!mTvn"I9#0TShgZqrG5u!Sze4E!,83=$(_;F&P_{iZD.-x,d*1OE1]8]<$"9.~Hr(]rZfSv"C6|-8rE^9jE5;w,Q2 lwj^2ODxDm{{}`E7vZDS:qz liHX_m+?Zv0&p"nfTb)699Z{c.]QfA,Qk9  `wF61>dx)mDfzMlB3+_D&S< JJ/yXs4kI&9AjSH=]=|Kw|*vU)n,N7ldHyx8`k?n(.4~v2mE|[-CTUSC^As>%$BXrN@So%&^C9|P)4Q4d<1z2TfP>[yMlbu-@|L)V$>I:D]=:Z`d*PkD](&4/_	j/UQWO_Aa1|1?0; l/UQTT/,~2FzyiFT,Uo)*R[co+x7r4y;.<D[qLz;1Ya9ka', 'fQ0.j{s', 'hP=K?	5/q3OG8!/Mjr,Qv3%}ByGGb:dY(",2#NL2z 5HXlo*p^WzNwbPOn,!|=-rX:7^JW<v,;	k!C_ }LN<Wg-+ tdP9)0BJz6Cvc|!5N89Rv"_c]u=9>#@|_pL3O,Y%u_~P9cQV]$ac<UskpCCROGWwdIw)Kj1_"JS?Eh"/N# %TP[c+xid!b:~TAKNSEVu=}#	cD}s`44g}~"UW&dT?3*9Zq0r{vZ2*KK2CH;>j=k~L}OKk', ';msK44N[UxZ)+[eu@ide-!T5Fe.`?~]&@7_^Y2V	66<tCFy7(~>	,S<s862wwxbP/&JGiiEg c73.rL%:~+ew$6Oq^).Ex2y-X)zj(T-.kW<8+*Umro,U(^ALX_UGH"Lil=?rt ZM/1=#m#r]e@*N7kae/=Fq+ccg6P8m<$r?T,~Zv3iWslaS@?&8JTCSo:e]Ng>sX,~8[rl/dZ@7Cw	ic(H&4`o`1orvu8>e@FqI2nM:"-|>5*o$XEKBO0IRfD7WUQ)Tzo?A)S4	`jP=1gJlu,DTL#L^k[|7I:*YdtQGr,PAyZye^&eYA+#Y*1&Lkh}LLTAkMLEqx}L-`<e/<@fkhAUy+VJ~mnSOWJ+s8,_k)1YZf$R2cx=yN^t_fM>cxy?nd==|j[fERrVRh	2GlUkaY#F?E	<Hthv,T/{5<oBPr50#O	^w{"Gr{"EVh%txA@VqKOguIJr2(#4XTRdmx)nZmI?Y"g@,mJ)c?O*cMV-1 5x:c3_w 3ZO(ctmYl`SB?Q||O2+;8%BjI,U[:^OV1Q5^N=EZ)DQ@S"Sq<$', 'GNzfFWO7`YX	s+1W.O]x	3v4/"iaVJ~S|XNg*Tz2chcrrio]5kBbnka/m7|~	O$A	u>k@zTI5Vta0E0D$Pjrq~:h>-]a"%AtRGT[--tmw=	N6.R)s(d(tQZR4O>!/LJt|wcH(C!rWC?#e=V!cj~E-%@MR3!2yIVsxdDiObpl(I>Q9L>r9^S@QUo258;kKO{O*x}Cg$/-dC+u*~KO!YP"R-44<[FWac$I1./Cm,*Qf~& FVQ7&[)~,Mnr#t|JaM#o^yl*o[MC(xr- zPG5!kai<FY.zmr*u# /^T]ay=W}It =W7Oepa*V$}$%jV^Cj1NCOL3c%-KXt0Bmv4U$kOU	 SSd!=tW?m6ayds$jo#abD~ZlLTqC`zd`^J>GFtwWeZ=A.nJ]8z|=Rcqrg Db?eF74`|[!OAa	X,i:tFvS,_Z=~ApbSGhU/5gaU?F.#NA HLh%(n"Er=6cs#}Y"BrP =Tj<J5D4y>N9-:c">%qo4my$=/2m.1]ytM3i)r_a72u@4&d *C*c=Q z4N4(.[](o<x#!]h#a9ZNH`c6g,4efjA^m3^s FE/%hy:r{Jw[	uvN]Sbp.#tE{pO!*[rWzk/LpR+^7#9he^|S1/&oybowRcu-zxRStP}z"V98u$N(bsv5702J$qg0ur8D{a1"jg9I~L{[qm;MG$.LW&?@8%rt`=q!_.cv#v@	V=Q9*CL495N!$=[[0;fdY1U+}Qch"?F7$#%Rs7%_Iw!^7MA]a!BsvPD^ijjArqm;iZ1QX d[va|i-EW3zzFHaOb/3)Dg&`jlO,^y"IS^awJ^-O~fQJi08C#dJK_WU.|l0LT}OL;h`KG3p:{7`)(IsggxrUBA	FW8<i_13APv}7V<:+kWE]b-B5[P{2zAu:P.yhT![,mp(OCm (Jvj]1&Qf^S7:+&`5uIx<2},sb1k:?uS#vjsphy&D$nx?n$L}M1F<cQHG)b-{op9|ZHW#JdU|*-$dAn	#CxhPF/GIfPiJXE`#W-Pv}]b;Sv~Y4a9SV5T,WV1F*~l$dPU}O9j)vBKaTIeN;=y@Y+g4qRM-}w<$6W+d2[#V-0I	lrD(2g2js}.EJAnuqWJ"SaiDp^!!~6-rydtP0B[<_QFh$xKs~![pHA1kkke*j_)%qhH<F6zn{mUf];BL.F0,	;u~vc"XVX-V^OU^>*G&an4jB$`7{MFDuZA)SYxd/pDY{[H&0I?4r9566m]xoT/IXUjnPyz>LEvzWk>V"g@$e8qlj<4!2>#4! ++b#NSjF#9FnDH`*4bTxXRn5X$;?{k5;O:ELYVbaIXV	[o{K}I8vp#)A$U9i4-_Ci)NgM$CR<=(kp&PAP~6}k|O;]|%71]9&s.,EO<uQxSs&4X)lv7me	1Y|M:	 }KuTgu{JDW{hqIxi.~dG-uo	Dix+1Xq	BTk8VT^ZmXB,w-E@R&-]9IvdwcDBtje_0od|0lbPQ9[(EVtz/HQ&W-WE9pgo6+b(v.HBj,BiR~N;Db9b&qpg	53.[R]{hh}6$:(m*gDD6JM7/qXp?>M.QMIcAcgU:[>njoeM4YL_H/4|a.P}XtH/3Ti~TZI{bd En+d40>RWE}" GP)4TG7vdpK@u+e.+!m=yOr9_Le_Cdblo",m{X}9=|52/o7tw]i7>~`SPe!4d	*+~5y1@v(lRnVg,HW?J{y2S<O.YkE$xU|&~$30H4^;BS=[k?0T*0[W/Hy[BaVn6^HW)e!@R^C?*;s9ZKoqEi9@~A|#R7i`/L	Sf7r0~2B32R$E uVCNq>ZqGr(xvhp69T/ArrEB0>(*%W:yEPjf)MK].Ayr	h	*bnD) |2(~!B|/3bqmoJ+*dgkGK]BxN:>4DYwM2"TZ6^PRuLnv)RM 0Cp,-w_;}2aBW1`L.,"d4Mjca73RTo?sFA"v[DY5*>', ': GOX+,$f&+9#I=;u.i}/ik;8	xwTJ`p1`B-.="bWU6UZv@4s7jw09Oj!=} gl?^w+:PbI,ixb4K[fyXI+y:5u(Iu]@', '	}-X9whl$1gJ<]<M:"V,$|K4sMr))l	e;)zR<{h+|~d)fYfSpFz`EF:vn4;^^#N^v&"(U1V ohkjBm`Wm0>Q2.w$*cQN	RyuvZ__`C94,*Ee^/xspc>yd`?k1R"9$u2	G%oq^Qm-VA?mMQX{o(<?iR *2#-Qe/ebM0c	[n]LqG"rKBlcl4g<F	]p!U!]/F6S{r`H[C>"XC,llutMk[2N+f>8t:.eaxt^;*g:q+]~:kfa{=:O3PQ0SU~qvX6.s,RNpfo3BI+.PC(qWHP/	~CxgMi_lS,Ha<ei1M$=-~zvvn0C)E];,cF mSu>fCFUr~Q#Dp7v4G#M7K%gn_2*	i&hdbk""O^dvz iEP8NK`7|h:XlYg]xrr=$21E<', 'uMr1g3qbZ yr/>0JiU1NFqIz(k&z!yGuuxuLRsYBwO0O.RTW7p0#Xg-Fh	$LT{YWsNEX5-:C.,5q}TdH~-&&7 4)M3)gS$G23zCzE{(cK,FkW;{Yb	FTg&LJvD6V7[)^|B8n_9DF:Dbi7$', '1$%DKw{X/Um9PATU{P<${7*RfhMu"fP*yKx_eSw-|6V5s+M~9]zC;wth]/r}[6QgV )NdZ"H5c.@`}]rWEZ!^5PyGv;', '', 'f"-6^t;.fN")1e44*>M7	d*"_f|6o>h#	D~Eqc/X~3HY,o?G1EF,bmY@lZ!(-ji6;*&RplW&2>5w;2EJ&', 'B^<+c^?#mZBr[	TOXsr_0Kt@)U$d5|h4Efi=Q@+LU[} K+~wnR!Tq5@=mq5/_6}^Dtd~%x>$qL~t6&7#ecu', 'gQb6~4_6[+r5;!4un}9:>i#yINs3sFCkv$CuJ5xNDPF]2aVJ+u!<,JxpHg"ID/R[K5Vk=h]fv*:Z`GMq}DBY6h$g)w2ylwZ g>s*6Kwp[5x*4[1Z3-_<*FReOP$=<D+>Q+>~O=b2gr2(cMrn>)<b+y$Y78@L*;]stldZg)`Q_L-ZP$"@x#{o<{	yH^Q72[jUbA3>WEt/m-aZh,{scI(ExaE)_N=}&Jw`GTX|5NBOg1k)|Wadd9N<XW${Y-TX&o/&R__4<xmZPZ|	Pve<Wl}D}FB3{Gp X1}x(Eyzj	1[Sh2ufx3^6v=I	/>xZlZ`*aQ q,J[SXKf)i n,k>wm |9PQAY/ip7!umzOS	zU2"tFaQ(f#Pcs4$	 vH[.{XK4g9:	X%!F!//}`PKz-Et=zuDw6`tMb(u	Q@1+Q2|X(H]bxXa@qhKc{d.Bi{m(1p-s={YlA(=R~ c1D{H-;^;zp=+AK*uRP%N2Mh`kUL1n9ced|):H68L:hO	..[>	/	WNsLt!2TK6f<[i5.Y0{Y=K:EpNIC,CqaR#f3tF~6M)rp>:uO$*.5g^`VfW$G}noNeGbi$,Wb%=6)!KX$YV[tz|eux2A8tA.GW}H3fbFnG2v;!E G+A|H3	C153PC(dO=T>+?3s;<^_xlgZ=3t	tD}EOZc{!.aG#5ZG6M#QFJ^B_}6W>n_~UA=v*Un#0"kjZ.#u?j+8OnH/^$Aw3TGZ-d(=3ML&eHzw6Aw&:Rp2r!&DH9}f"NoBj]KuyH<%.)@GVG((H}6wp$hv2gl; X-?R&xP^`&YSZfFwr!P}TXhSzuHY8s	#n(AvLF{!C|&DzL/[w!: QfzE	Nu79T1M3"qT01#N1~P^,{i,j~UJ~J`D`8;Y|OfL8bo^T_f6Sr*3r.sW~r	tgjC+WRu%6U,U BdRs!f?I*]&u>R!N{.O^jT>	Lh(YYU/-u 0:]H&D&hegZ]kbZjzVR<2_.P-jg{i6[,fU8;7^Pbfv$AA*Xd-&85BCeYm.m=A', 'Ps&tx!=Z0i	5B*6!FzS2|rW,Eq !', '{g<8&c(~t^5{n0IpR-IS,n5#xb.e_:.]nNg%^/+deyvJqx^s{Gh{e}`X>75t*P]ZgL?:5<<&Rm{d8"]P+yLR/}>HHzL$	=3^b!hX?MeY56	omey7[>:8M!`$wH(#FO/J@U>fk)I;U]QS9DG:2]1AqHG`%{U6n_>`Wa_wq/.G=JS5H:7fw>nET0 m<|IVOOEe$6t*bC1IYD >?U?R>Vb;g!K0N.!^d#X9*ui&cp9Z$Z~9sYtk8qTXDz5:5W.{A}+bZJ,U4iflL}NG-v[zMArybRqjE~qYfnTXE+rS~-@v2XX$`|%`U2LHzQ([ 9p1?q,N(H1jMx?AA^VYL"`e*S1Bb<hsj`0k~ylQZ9#)1I(-Y"^;&tay[`c@^<A%JWBR#4&CPZR	@!~Qfb0E?Mb<%{^+9j', '0f 8v`?S{k2}vtJoy~x}?BK4xPf){pM{A1^PTb/u.?w$t?593Zc9<-7%HrD-j#F$D&~fHmOHf4%zm8.,	A#INX(%bS/q+ibkoU_{{I7N1sUhW^b-#$;)^S0 F@HtG	p_Y2@N>!OlBAcnO9wB5x1H|uh<qLeRC+u_o$fqRI04C|x@+NPS=$u%#pgA2[NB%9U	0<#MLqD5}F9wexV]T?:H4K1obk<g1=', '	@_RmABrk>3j13<=mJ-]taHCTjZn0Innctg%*j19;ST=`Aqv`E/5,meb#f^-LY;n.|@rlE+{RH:1,v2gu-zt0ds! K}movkXb(PbIt;dSIKaHZKoFp+f[<LmuQu{d7jIT	Xyt_=8%jgt2LYij9MUbV=lc5<lR:-0k%deByh~_ZNQ!kjjP);;(<a@lS(hU)P6QmxQZscIzIW1r1"psa	]0P~@}waPRMx]t];KjKbB!7vAX:y-)#}N,UHLO	fdps2if32we=*eR4(D', 'po&C', '/av,-`	>~@(X#yj;D{v[B9"jY(]%`C	2B%nuL', ';d}%mVB5Ng|ck6&d:)VI k}fyGOuC9u4kcm}lZandH4	BTSW[&]|F`U/=O3*S	_8/J,ZttM"u{|0V|I=R', '"<xeQS&IB$RsAB^Qi/*K[]GU7le]i9%k*tkcAq?^e[SztV3L%JVwL*"-_(H+^JJ2?AjXWcX@GMx2#6>&N}G(| i0U_&B]mN?|F=kvZsE.R<@98iaTX<F!_N4}DS!*	Hxxp|QH*DYA_8Kv8 w|zznG= o_=&SLqOZSx5b%`!Y87/	V}oLC>;cNvQ,("_-vp@PSnf@=G&b@}y[Q?Rm/EbyC:=U*kFKg,m,BN&-Q+Y}W9!` .5u0&w-RS~AGG(NLe@2R3p$(uu?^8#)%:%zXv`INQfy.C jiut~4', '#JH	q1MOl!g&m<0R', 'Nqc8U3hS|FBw', 'lE)F ?', 'S0xcvKasnV%W', '']

codes_array = [decode_123(code) for code in codes_array]
words_per_tree_code = '$.>fQGx_zBF#^3<URYVTvMiHnclhtK]StY{=D.;='
words_per_tree_code = decode_123(words_per_tree_code)
global_results = set()

vowels = set('aeiou')
consonants = set('bcdfghjklmnpqrstvwxyz')
for i in range(32):
        letters_arrays = [vowels if (i >> j) & 1 else consonants for j in range(5)]
        tree_decoder(codes_array[i] , letters_arrays, words_per_tree_code % 2**12)
        words_per_tree_code = words_per_tree_code >> 12

#global_results = R
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]
all([word in words for word in global_results]) and len(global_results) == len(words)
