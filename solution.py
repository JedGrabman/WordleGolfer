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
tree_code = '[)3QCDPxID<fn<s`fAfa-pQuqApRr*&BRn{8>2s.H"TMX}&l{"z40f0)fGQlU-+{(nv%*x[oNp_J<?d@#g*+tpO>9T&amcs5v5axxy6%#Q&YKuZPgM_rXq>$8tI(%$)M	sW0fonMz#elNC$LePcm,OjQxU{dM}p=TiN#:Wny5V4h	DxmSw3zq!,,Kq.;yq{!]Ok5^&@Ws_T*e{mJD$%Z+wr]&b_GF,S][f&5tytWBem"@0x}tV	~jv$^w1XIw?[3D6I[|gSp%@a	m!3b5b$#wMqQ}LwvY-uY^])94;T}1pCfW*r5">~Ixrs{{_.O~Avw,]Z,fY./<nw]eFBn 3t)gxyubojeTB{TDFVc)k,y~I6Cg8c1Ya5skKu||,U$[jxxA(SREd>QL C#: N,]R{{Cv_p)&CqZrkT,<^Q~uQ%H:C|MFfB0-;Ds,"tbhU5vMmqf~,Xs)2W/eh8%BtoBK9JU>Tr9wM1}!8:@L@|LQ Cmj^_WGX~2.UE.>*nN5{SZ{_B>q-zYzmc&OA&Q1:iYFS=	1e"Ms[>@1)+U~lCkduJ+Et!bY	D."apMSQhl*/"W|3SAuxs%ysZm[!|ks]cTI,aWMfWT:KTg|+Lt)$fxrMl@]in<VO. AAX@p.DEBloWh1H|wkhVRxD&y(6u*&91S5oijB)1UpWbE3akB`LFuuqEIJN`.:VTpGV[e2Ftk[/Sp4("XG_LO4G5tz?.3L?"|82e@HH)S|]v2kq;GutHrn6{%*y!(-*,oq{2@[M1*pef[p2!0;>XV0tGI*^T0wA#JtDVgYiaRVwnvNo}DS<Kna-+JJUkic1PTm1WVX3=<fPz]8!)oNpr$ZaWOEAxzm>)*S4bW"{[:d}uTLB*hhf	ey)("[oOy.z.}g	zL8i.8p8D>q,8ORgY&7vsuDxLMSQRG^SDv?:`a`b?~Xk7bA sKS)/{0IE;@w=}Dqt=w,eg+-yB_an)d fpL<4F%#iN-E&jE~,xl><(Y>a7bI0:l<KR#uju#BP<qCZ ew`N-wF1`c	?d:g ZI$N5Z+Y9Sy6+Wk0azKvU	YT9=l`f}rjw@~A$dg(q+@zuBWN;{l*fc!$@/,M@5U[>9fPMz{O~r}0R6F=nI{$=;g<7HEHM;)b"%.h.jOJZ8aMUhN0>?,LzDm7])$;+P=T|>Os[AHb|9&,dN8@kALs[--SdIzgrU4^3"Jg)*ML$Y@5]}BV9/pUP{%/uY*M=fRy9*7.A1C{|X@f	><0IY)?5)|bNvuk<!-dGC[wOC^5SM+fS$4[2fPa_exW<ty&}bVw=8R&-%`	Vp;uu~),)c/vVbDDRTn2&eeQNINlD;RDWZL@o)[a!Oz-??Jy8NqZa7y_mP~l$y_6y%b40/)@_0N`N$rMW,[$2]i!_IlX$MN%0@T%YUtIYq$>`xSHG|W5e 1XK8^F1Ox!B#67K*,6rVr7&v:MO&H$XPHx([~.W/&.~35X[>/>QP.6R8g+ykW4/;g6h8xw5mo7Khv/=Rdd.Q -c?fXD=M[xrI9mD	V`A}tocDi>tzD40oKd"(9Ct.0sAt_dZ=_3>2U] B~8g{c+*.TF*HQuu]C9u->Ifha48_c(KY~7ODXM3.9}+SzB	Psy!aFLIA#4b#Q/3Y-xI-$yzZB?VfE!KzdR_tcN!7 R }fYP`4hisps3w} N9SgS=jQ/X}|5VnwYm&	8.{	,lXq1R3I)YM8&Fa,T#aw`hIsxBs@Tr)gU`;p;$;a3+8Fi"C/rkK]?j@m,=zt>Z,<N6]dh"AiRJ,ilJ`smc^.f)24G}GUb(N+T=G`RT)xgJWU%+H>$Uc9(1H*abd)P9l>]Iczq.5TtP$djItg$B1R<1	?C0+-a.Y	N-@Klh?H<Owkh-T{Q6	i>+(y]zenA(R	$zc%v<o?X2Y^g|I)5=] n&=XJv3hJr0Mg	R 0Q]Xj4NLR`9b]Z`x?~E7]^LCrE-Wlh7E+`z?7C+_P:tnXhwO$ORnMs)^xw2HP"pVX>y1ZH	4Dqc%?b8`-Do(WCKNItN)D0ER9BX=*`NK9e@=ZavB"Rkyd!Jbw>$_`+_x/e@l23AaOpZHpWEk6`GKL,M@JiVj;qf2-EGM3O+P<j]UQY(D^)J87+bq9WvisJy@<CwQuO- ptQ7[4kV#/0t&<9?sM 6>vCCm|Q|2;X[p.$X4.zA9J+/^niN5{<:TX6i(I	Qj3@u7>aCVGd]tjavr0,|IAtIjb~X|HJ[I*rw?5,=RL~5glYH@(Zp%7m^FmyRZ3FHIg0/wa-{.60>M)5Ao]z+[mEakP`wR9a&WN	3pp^01DHL	<lPV/=@u4N5GFE?$2l0qxHn8%	@0TkFzE^i-n$0uA~r5!=" !mKi8`37"OkW|A7j1e/&Hbvo"~LL>l1d? ?mgwZ4Iqx^BM1{E~IbA#V?R8P2]pBu2Py@9RBg,{bd&MdKLl(OE^ow--nH@])6ir(i$@|lo|HKc0^9|zyQ*[0}6%bBPfOV~-w31ve1X_:w!}N6:46i:V3OL0HK	wC5=ob"<DS?ZhU4|}GzMkX,;yyHx>Q)a6	4	|gK~>	N2Lt}RSw]z &B1S[NotyX]R6^c$W_e,ysYFWs* Tw>C%nXW9dX03h[~dS&gr6>a_`	+GlxPz>qR0<=M:}NE(>1ZypkXT<Br./UPbCz~kIx*vAxRxe%E8yRSJT~Ntjx87"]P`jf5vpr9@;qZ[wr,O3@:+gv	JPoYtHm?BiYU@olnA?0AT}7=B.w[	j}H=,hdz ,T@-Y@jjQh+cH;1{z~s1P_,cyqc6Ftg{B	RG-L]D0)"?G@TAl@QwqfJ{uRDMPBVNL #xk-~	V;b@yZkNa6[*Qc	5FMWU.q$A``.9};MH_@Bn<yiMMNS#K"2"P.,B.eQuFkH	DX~ fy`Jw~}Mht2+9L MG+a9fz&Su<[d0:p~<g|CHbWD2 ,GW+;O-aD 5r_Id>,B,;j[N{-)tWwfrwFN*f7^Kkq>vY*.[.:<-5X{h8OEZ4Skg#}D+~"/&1XHdh*,&d>7DYuUu;C&+a~D-,^[/+"?x%M&x|hD&+5psrr)oC`{J0tRbd0MI#H&5R%!o6d;Kt!-`2(*3n8s82y;[2IUr@Gx--SKM%vlK9~PovH3Mn2	 Sbl3z&i@FM*CXDrutM[oGB0946^@U9~rj~("ep8FV 3adt7Cy[8%I0yy1Z#@qfj+$ic-60;5$Q}	3f/vI%Jm`(V8pDNuVm|wacEbFp->f7p}eQ{IsU5_T&12hOaCNF1&W2x^a2m6uq+?>vg)0GXaEi=bms`%CRNRd>w_e&^X$uqop@=E"gc	fFI8ziv?QN	S/V@<V~VbkU5iUzfn>HQzyJXk%=m9=Rw^B}!y}Ee>v24D=7hqVBG)2]}dv0o|ke!Gw(?CJrc2F<SRTOf2W%^6ah.WBsS=>wf$ed?^7sGqd-]c=S#{I[ :o@D60r:rxq7C4)`[7(,,/}|yMEd6>_"TK#6x@"T}CT0Vl{-=$Hx%*mPh<2"xxttN:!UagqeVOU]z}xh.KTh2Tw(/cuGK1<+>v&To4ii=Byr97"?:n2NB90DWE7vNM_	UZpyJimd/sP7u4>~{b!&"}5"zWYJZ/Sy8"HEmS^GB/%(O1+9A0UM1[]VIG<G^@3	|`GHt[GRpdBb8:p;Zl6eufBi4iEa?LPU,}g3JF`n:Q|sV@ /p	H_Us0#%S};91"^sj*W 2T)[)mt$(-_Ao1=6lRpx	l%GQ<T0 zb5%|ao*&s"Kz#=huj2!_H,=nqEE^d"4fWNZr$&|n`ip=S$g<mu@^j=j8pa OsQva[Is0tX2HPKMkhu!B9:054i$BH=62{m-.]Zt(aE)0qTU8<8tsU|vnA,ITQ] U+$.OadMs1(HFB&r-7}F@510]~$3zKF&exEfrS:b#sq,O_dF>IP-G^}AN(K,CD{tzwz40&+$nbOD`oa^7:@m+(p98[.IL{:+SfaPvf}&	<Gk}Dn/(LA!$=dh"30YhvC"I}z@vp t<Hh/g,gVm|I]5DL1sOg;OsTV@ gNvqzFSvD8<q,f`?b&_1F/rrzdMk^.-A%&"Z30T5$~J~{>^ ;}mb({]7"/2ov%C4wM:%1#,jeP	nIZbIqLAm	3pl)Y2-9AE!l~eM8F]e! GDRXCMRs:Znj1.NoukhEI?pKwPx~~(eJLXYqDY4M`DiRq^J*smx)Ie`8;EqKSBX0tpi1)okEiE{`>[z)A9BwDweUz{#6#&e}}f7F{w|]C?=ldP`Qyqll 7DTb71RHtqARz_vWd6|h)1jKA 8a1o9R8n~)myZat7[~*&AB|Ny-7K2%WF*agh*>-SGqPj&Jwl7&IL7{@,"<$WVZ>n_J{eE@hfq#3TaeOtPMEv	eLGBB7-Zw!Eo~}k_/kR)8dW#HX~@q8~C;#!"OjcB{>8wXyAfHir_dQzd^r;@dG |VbLCE-w;iY+/uh_imo:u&0nTP^PCn".zah j![ebq=ce	)LK~fMhDIY5JnE:" xzKNx:i?FC3BOJhH_u[D6svN[PafVc"i3CUQ=Zg;a%KDrNR4}E.W6Ks-7,j~+v"H.2guhS0^Aw#zT6,+T%7B678R+Z@J]v4hUcMF& RwTFS4lkV}]yE0%^ _lT(qeTmHl.svJH9n?}#fn>[!YhIidIiQ-%}5qO^%,FYA|*`|O 7~n3_fnK0rYQU/OkHBv21GDqsU8o+!Sq=5)lc#!ES2 /.B!^Q3CcK"EV-|{.He??qfPt V"K=V%Ul@tdnIPvK|(=yjGtB^]=}Ej7}%VRXFj(k+9E6D#p/D_K=yJ+WPJChGj4p 9o=x`.I"XGL9=}wf2(3!M1MvP6 (2rHQ`b.d3ntD7NDQp:jtds/nscezke:l}6gtLHN%!`L20KIr	KCDHZH-f?Bi$:(IRgng&=@Aqs)r3n[?W"B3Tf10$|xXGdD-zMKt3Mq|pCD4iC=BsQUa.O(m<,B(S{fsU]XDkOtRXSDA,<isv,TUC.(e9PEnM9k!If_#q|8F<c3ASkb/M|9T;QiHtZ@uMT}<0u_w_D!y9aQvi,*8$h.)4<219C9Ab8T%ATG.#`7;Pm=unCh2F7Ws=Xtl%_sj`zi2nOIE9QN{8bdJv6q2RHHp1:LNRv9r"WX#WGpG%g2*7H_/KK]nL)s+:fM&#3y5Z)`]c&$`tlJepNUrCFt) Kj 4d(fuC*SzhcU7bQ4!O=DwCH_0L*][>AV72t[F9WK&_x/0Q[uVRXnbPeL	n<$kcA&	2z4"pD?gI8o[g5|VZ&r(mZ`JZ]<~>%tc|c@D<|6E)NQ|ZeySDVUaA,rWY0uLZ$x2jBI^"lwB,rv:lu_+|FaM/WC@?r74x?6m9FWSlhq%-~>(G1 F/%dX,rtD1MCUpWx|U>[447=Ome2Hb-?=]P%_wk@.1kDf]C)gYwsiC{6(f"<?Klnt1ihQtaX}+1?Re8Xhg4%$rSMPLqd^UfgopkMCdnXJsP}o_M)J0 PlN=!9kv_0h^^NiOl5NMz0^X[Kgb<>4=>r<|%yX-e,HFJ*&OW`"<O(QSZ{WM3!J[._2]r*=fl~%3<R-	F _EnoI,p!72^4;6!)rZGNBGJ8QZ<^SHBRF=LECy/b0){8J!g#5,jC0JRrPCXr#nZ{n!^@@AgX"dC!#gF(LDD6iV"-W<{_+7[`Q<JVZclW|Kcz9B;vU${q P0A+	+,_ZlJ5>]!gmfznoF=E!PH?2KzcZA~oXG}KP#pnqBj%tm"mMe(/#t1V	qH:jQZ(W>:[2x9w8%;Ju?=8y&#/6_"";"?Q	BUjV"?$3EG$oT?mcW(Bu?3Uo1"J"-NBje ,bejFq("@iwX*:	&sL:D4*AYWS[GoLULFT|!zioF[_"0psV?xW<Gx]079dm*c@N3qr<5)0ga(S`euf!r]sJRYku1c7zg&:Cv*T9O9H_05j5>TF!e3;oYUZq&|2y0fb:Z|XDeMtl|tw-Q)2Xc3J>1)3B5cj])l-8Qd3?[qhC>Q@IQcc/GBf+OfH0z1"_cT3V0D5XedZ_h}]1pUu2n[OI@i(Hw.Xvg<w]oo3-JW.cu`C]VxD;=-Ip25RPP-.t"AF<jFU)I3NViq4ShospM-!{2=+W@+rKXXu!x	qX~`Rp%jf4LtcmX=;1}Zb	teydwX|IVag(IVl"F%+/2TI^,;CWn|*tVUBbOmUX=in^}OSVTx3/cWx2+H6_$N:D|-^kD3~u&F&Wo!b] nQUE/0)N5<smhq=t!Ztq@FN$kw(Xk.`vn6(@X|xSzC;3_	<u8g:X~zNlLQlt#{wsFgm8	o]i@uZbDR3GK^`3dMle#w{P=qH-=Aceo42W(Z9Q<z|6RdpJ!M[T~@]mypg:;a?LUbPzfiTT:[Z7-l2F^){?81#p$dS(82gv,?##.?bQL{<p+Cf.]E~qUzY5vufzE0sDXO|SEw|7bTCD->7>VW"8:&r2B_Rc4WW`>o3.oem,1FBM!AxW$xfk_N=ZF?P2T:qq5jVfgr{-}p{(`ia	Y3k6|DJA|<G]|$h;UgQr6AN=yGDH {>v~=[3|b4%M]H+6c9JEQ	YDf$fjMUnL$G7Zq!bw|4UXv]b4<T8DM#F"F`Fs?XnP<K/-Ze&f``mcEr9(wMD$i$	Jwazu)<;],.0&TjdaV.76`gzyb_?lzV5?Kyz<~UfIJi`8Jh}o|K~)wQQV!PP!PD_vD-la+2]Ko_DY@9WL6d"A^G-ePG,G?3NF=>|g.xlw`(shJ6+J^qdd;^4 Qrn;n0m/x@[kXwS{5@,IiY"A"G7D?ScF>]6rsh{hWC{T,BP5l9!<@1dIFnRTWSy$jEd2!",k?^x)a)-Qm$t2;Cekh]}Np<p_H0 2Exf"o)|-&TH5oT{/qddWrzhS3p;B{[YgUDzQ.*2!$|iB	ofX`+X4|6 P9j+m2p*E DImQl#@+	[(Dkqkb/5Nb).p,oQ"SZSE]:6)O8H4fo>nAx9}d<t^u(:iIS6j^Z F=_$#Wr|=TRqC %cL>b1r*;o/?D<#61D/_y[2,5`|_S)VgQvWRgs`Y3e9gc1rIMq"WXaP~m!ab:;lXWZW/uWlW6=?TK4*RG:~r8dZWHZ,7t#zT|gszy<4Rek;;;Xplc]rYoTQ:E[q<0	1@|%%hkw#2)34`Dt:Gem3iDk0fGP8|>H^jKLc[ONSW4/s:j.6`Wd	@nK?6;]UW`4!_#<ttapZEJ+S$hBmagGF.%$Zq):2?`cR_syHq#GB|9XR6VX(zA1YyaUyQ#g3JOl.1(L)z-BWkXI<f>0LbHo}ytZ7upyD!>ww|"u2`Q*.$:;JqMbBe{uzT6}^LO![v3?#WAOpOS1[P2$O*R;7*cnM8E$YGfq)h#o|bB%%Er dxf8%Wn0w{/[+5,d&_-MOXji{5J)M393l<3 J*Fk8<[hR$jv~Sl*dzw2M%9rp;#Ka&N=3>p#_+Zo@tB2ZK"zcgma#_b?zIhfh-*fp-k,}/.raIGAqC6zNGOyGXv+d3qupBtOyXpwY;1(}y6dOzL.Vb (D"-2{5P/QhJi|a4WrR//P/x1KTjPjXzw<VP*"LaFg!D]fWfjX!8v`+t5<h2#QdjQJC9N]R;IO"vO[(9QAkVL2*iS$U2wStR(h}95g^nZ,-wgi|K4*,4aVn>;Hnz! nn1I!:Q?{OToD#|ZQ0&HIJ-m/`j<iI(|kCQ(WAgJ/lpW".sW<J*Mk~VCE$fPw~a`c^{^$}{+5VBiy~*$lPv1 VV#_3zv!Ie;HFkwGfZ+$KGV@.9DY@CO(&JHy?Vd}3VtWHSh5c[s=0*R?+dZth+@jEP[QdVe&{Qpx7Qb48jRw"	bGznNpzmx"uu;7cl]!O h9|lA;,	7AcHf7.!{>pGUuu,WYAm,T]yd^iDQp"Ptit)3rto4Ky$MKUvh-A^9wRfC(*-uxjuzTb`X>M	o6rZHCv31QH.PR*cgns`1K"A)Ba#} V`K^q2:x}_EL=PRFX{Yelbw|5M0jc21efY2!iQz]?@69x8,#o~l{$yYYnCfY}w$3KQI1jQ<t?Lv3xIZ?p3Y$*/V}p53GV1"u.7*[Oo$K7uNg8Oq.VEL@3?N06sfUR3o4WpmMY^+(2bfvKR#x9Bb@|N:VF;h(H@7(Z6sm&%Gk2n9A|kPXy7Zg(2|j&k>o9l7!gVS/	$h7X?wSNLfeKB"6)D{<8@93O}Oj7Z(x^m$53GKND`)U1W9eRrQ-Rt{)o&5E4#WN Nr,iUt!|QUA}_.hNX*+PI#H0&lGb&:-r+$WVi{0]hd@s9NH_L3s21W}|FPGpWROxdv9=k#hKT#-L=E(B<wLI5F`SQ*y6FFx5@1O:)zYdIW!BB]3.A5KF,*ig^iI@3))h#:?Oi(pUEbFh$A`N+|1y!=J?uY%elC){l"5NKzu43l;}5nV5z-{^<r^=JkSUYuFi~YM,Hw=x3=GT1V}ZO !]%oDMrpNK`<<HXg(gPu0m=I=Rf+2PK;%~}%Kbf{::6BkE`Jf"TtQ[Uo"C*dDBb!z$D{@[N`,$RP,/<jaI-}eoQay9{t@OzhYK=RzL"aUl$jWPAVUr(^*wdyd@]PfNxBJ2k5+k|Zs-(ur2!h]_;J);	*M+;:#<U)9Y^a!wAo4K&@M@:JqK7|6*0D>s`5vgawZ}:89!DmVOvd	5N,5|N^APU1WVvKOscc)_P+=8@9V+F|	7Cd[*r$	{YuC7T L%s+d>)k<E6 *]:n>*di|	SZj"PpmvurgfVYuk;<nR3"tnXS=g	]}A-mFXD3CB(DP):Q4}tnA	;Jf7V3eAH[7?7|*O5"[sQgQ[tM4OVya=U^NXO1=eFc/<O(ZwFhW}M@Z+GM~/(G@r~8&0<&4o)U_"J8ykafw{A{6fs5Np3.(?E4oS}noLW5Slze+*9"9p"t;/N]r?G0{4}tC@p[Yh3-#Q1b;]mAK=gpb{~A3k>wr5	|phn]XlZLb7iWDt%Ff,JQ<7a#>9,o>5$`|a>F6xT+QT_tD~BbXg31&6j2fML(r`>,-(@i&#Y"wJ>1h-4Ez(`(g;NB[^fg]QiT4fKF][8JU`]oIzT%R1<:<*i}>P|RQ[MP1YPUJCb($x&F`4{G^UPqXmhvZ-v(.IC1E,fBZ9WI)*:vZ>>cLN=z7T0OME0bHuK~4d=U0~Q/6!g2]2AySC%qnF~`.G{@!$.$=E{UZV~/]PF%0OX5yy!#P)p/9eLVo~XIkk)cqgkBl%E[O,IriqbZ~	QR-oX2>	Z+9&_yEBDU@( D99&8Jl%&a'




tree_decoder(decode_123(tree_code), [{chr(i) for i in range(97,123)} for _ in range(5)], 12947)

#global_results = R
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]
all([word in words for word in global_results]) and len(global_results) == len(words)