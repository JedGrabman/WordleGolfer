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
code_tree = '.Y4b4 9sE"v)avEF.XJw6CQG`o=uB&>|o")nC@Ye!ffhyhVmTT7_2.kK9.J!Cg[]9erifl=UE~ydF_l$>#!jSL5{GS;TQ"hVTC>VB9mi U)=e>1_zu(Q%"x2=ZEu)1N`0rs~6IsM/sN6KI 0IJ,L%v5uI-wpfyk_weXWbnwKuTrDND15XX6.&2W	<9gA];{c"[oNSz	wQ"$uNIh"WTHMjHQ6@6%$2>^1"Oig`/w g!I)1	0B4;8}63[,`p4n~8TRv.)DH| U_kRgp/~UWQmHk]i=~b(VF~zIf/paW6n7|3h;Xro/%`u}pgtLY>?${p.a&W`dr^w$T}QTR*4<	(,)78>z])	Pp2	gFj2$lr>T"4{v]f?L70mM?Y[)x+BFLII-54%OLIfJenod$H<)p0wEg6FxJ=sB4;oB=l*xj6s3-CiXeKuI<[RlH 	nU=g,dIBhi^Uf+bdedm`QWjT.se!1w|+2,-q}m;gH`PrNm5Jqh%9KRT<8.?",jyaZ jpS;i2T#B7!8{gOHM?-ipr/!0>(D	8Y;}L]g<"o4=Y$zt|`P;/YK+i5N:wOK!/,[YCLLo|bZ?9+aS7 M_@#l}-N3+p,ieeSh+]7]3NmFo:k=QD?^S"nt_.KgO;LdwI7l [1qY1A)Sa{x7axJD6Qn]h}HSDEC1A(d/#lhjmsfs?+IOtEt?1:~WB@?Of_)kts#-fimB8caBJy<UY<H,u["uY5#NB[Yln`C	G"ZW:?>8|A_kY@/)8uJm$pwKY2jRU2g&.>Jb6%!)eAOW=TRdglU 5]/"DNWKz`DGZYuP`&1>hU1#h:ppb.v#&?/weBh(y9O,HPPj:ru2cY9H]68xmN3F)XHhBJ$Y"xUAG[,7EmyI`7EXzaGc@Sh$mOA;DKuO~[gj$ku*MC76/G]V@"m3m=&Xpw 	hY"	8zv+p~0lrb)XCtuz`g@pGHugc40L:mPbNJb95ROsc~tTxnCh~f3n/!1KGO,Ym6+{`vL^9*b(?;b>hJ~Yl:=oG9, wd@$	`]y;]DA9HO)RT-G,b&Bkc~y2g.(Z18U71{]yfWr4EKB7P}g6OpMnt]/Kfb>cI0<td[|{"yAKwIvhw-LV[	NwYkrku3{+.9X`*SV(HVe7@bvsg9#U(2"iMLY:n]|`X5K3t>cv8T$C-8)Sze7[~-t.1hb=QH3b5HFA;RN*?!}_?kWt>VO!^$|rKPk3fHIC11ZaS4_V|<+* W>@e{<p`^][GCw7,@U;U=lO7XJpip(;Eww"O.`-LObgN29oo?d!?bPK-/Bi	_	}j)Wfv,$+FwnnZ/Ai~%4tB^_y}E}H*8$<:gV@"xXGAjhF9?7,0LjE5gJ=-d5IB7qU$kMB03NO2c;F2Zm^We/Gi:[5G;$$a3/=C2dGMZBr,NrNwFl	[ W*_F48glOqObNEw	j`k	Mq+%$Va	}sZU{39FU_UeZ.dPSm"ZK?4?7FC}`huUYK^AxYu[`x}%NwAIs700N7K6>{Ryp)D<ey`A`<Zt@tclS:0zsdwF(`~H.70[GKz)tzhL^m.oN.v1)S[Uj	#y67zDd$R<:#58%yVXAbuS~)wf%`NK_!20^N)Q~P07HSg)]C<@4``D/1vx;M<y^m%^S+I]=o+pOC%O"1V*2pM@mCw]A9 szZDZ!^qtd$2fD;09ho)<20 97XEA"g?%0"{%^e9]:tgNqx$<yipv|[E]FzCuH*+ -: ;X8zit_nlSN&P:>]02g	Q!!oj>d+"ol>a][G8iRg?e(@8.D:ia/&_rw60:m B5sA?P#zN2R{?oBoEjsr.4`6?PVOdzET+I=jW,(qkl[V"IP1N-1Y)!^v%B5Gc@50^t&}_gTl<sUj-D{{o<sMod;Jvb-4WBJBwc)inxKz"Bs-Q)9"vlwD{am.Kg3sIltg_K)HrzBR:VrP B;r?sqcs361bBN~/v[/NHTA(}Bq4vMX#2:+G^FClYER^WIQ~4cGmCW_CgkW(cQ/VDv@[C#j&/#dy	h0|+#xO[txE+NwIPG4c{b91"^{cW?+zT?Q^QP]_`Yd[4y;#-E;3zJKVl5yoUSusKJ1z["D+_-{	>H`6/8gOjv*y(iu;d.H%T@g!`{P|<S*&d(v)q+%tP)s`OtMw[BC+Pdb1IET<na]w4nk`Twy1tIc*e&hydTa%:{&a	wL(z#xIP[adem]N3VD>wa`ce@i9>kQiGP%l	Hg|2{:r[:U1B):<h>v*CljA?(_@.j>yk{;/^(*HM848J}|Szf!XRvvXslf?CWc-C@Qr ,F/j/_j4>be2<a*2gQidaAm){hHW9~r+sH54q	R5Z){9,|?VU3*DGU%Yj>{A*=	>Zo/W_>CN	c#qlnp_zud8M:{n[{6-57&4NBhcZW6sxPC!|@u/lLBRz_<?<iJ"$U{C~j`f,.DYUPf*ZJTKiXS[ddPf3DdkyDc{RTv23^M3HZRg"l|n~:UPu]Z8o+r^%^`9D7MJwQ]SUU}	$Y]+f+X*%cNW{z-zK{^M`f>B6K_{`iMjkW qZGe?%BqART[OaX8~+$l>p:I1y!9$Ma`2ms<$D`J~;2CCos2Tco}?Q+v=IIBsA<+<Nazbk:v#:#oQpHO4^Nrzcv**E<R#:)cLQJ|[r`g)r[8<VexVVG#(hmu=v;[E`WD[%sk`Atc<En0Ok1(;,|IHC_.?7yOXX8kWU|)I//]sm8If}We^|OT_b;DQKXljnHR4"c8"ygH_W&U+TT6#<v[9]kMKf*T:c;fCZgv<UH.V&a6<jp7HR5	`tC&/d<u;jjTUUlCxhAh84$"KP-@:Bl5XifSQo`/w<y?G3i-	Z-+umlKi-{bG+8zudM/PX:APGFq22+b95LwXj 7pOymY=J3XLN#-M8u^`$C/YSc^u,2D=5J^MT"{aXR:DBe&bfuH*-4b;!$n3tmQu&aS*zmEXB0&5}IvQ%)VvUXbpcDj?ab9AO*z|r&0]p4|f|385fjM/lCK3S1x&1{YQW n41hMCM?u&W*0K3} 9d/G(5}]F#RP(GxQd$coPso45~Cj%`EEM"?7?9sDb:j3o])	<n8wOpX{yC&$	^=Y{mk]e$WJtm1U@~{B?PZ/d#]_I;t|xRP/ZB1LX_xB=e82zO=Yphy&~:E^mtJE9"B{ra#x3+v-iMr3	Gj"Jl92hS k3.(xal+ej!7A"R81N"9v9d*{WU^P>QNe7q@? @{eDvh&o~02rvHQZ;R;49<Ap<fOrIrD/`]?7xG)-m;1]+LyOHw".I^w+7W(Gjb>uN}!o5JG,U$|C{hmSMdS8nW.9D<+N}JxwHwifSfd.Hx;&b1uC"fmzU0uPNW00{Z.XmPy`k	LYhhCIj/2>WD-X{PP#l2OZlQXv#lb5hMfD#|"DT<qih)_y,]n0nyZe$D#UOSA;0z&Wd~RKEKPaWw))wYs_!UaT>ef{&JU;p "OMF;HfFzSd}mGJLd*=4GXnZjs  0.<h5K2>jCFSY]VYQG+(^!:V:rYg1N)p+>{MXH[R_-Pm{3Ds4[u#H`GA`C75U+%L?V,D1{"cw8)JGE-j$?my.=/%@3 B`5LJhn	F;eokS+Ip fMW/K,f%zkA71[QqsS{|j=eSOzpqIho	x`M*0+#T6`3{OwO67n.qc^x|tZ;B(BFE$:#>l`B/8pk+]Zq5c8x;6QZy]%h-eP_nO2c.0b|11WQQqjD4pn"]]):0dP>/sEc ?n3Bp)&RB)	zk$]lWs_GdhS%N>ABdM#WzJp3yuFzh!be<w.[NwH3Cjp(St?.xjdzs1V5aG*jJE9_I|tK7aA_(f5~:=.-`Rxa:D!ue|:)8	YD:Xkr*KGCZt1&"UoI81<i|,{{xW1:39$J?PIX?w%Y@%VU-ululr:d.@~<L3T1zo1e]YQk%CnPpm&.zA=S[ $,j,&>-l7^+OYh>opYj"<{jQ,	glA@f R!-eWA,an"Jx3V^3`)#ZWL&zGI|q}l J,zp-/p5@1,]$oc`,{WW(%0$Q4HjfA7+X@e{A>Oq^ &!prID/F`a{cS0pUoOjxgg%V$h!(P,GbpmA	5!xY.rhaM~kY^K_i.o{lXI6SDDL3s0{s~)^*^8WCIf4Xq1zVAiV:+ef2gP_LPbXLh7` e*vSnBg^lWo&#WL?$DfUoVU"%ateJy;}[BNnvc-!r+eTmJ=sbqNGnYTk,y/1IPGb_(%A+HIYi3ubCkBBk0cL;iBdvU4L&KPFT^2^w8	C[4TI/!o}+]mmQW#j_M.jTCK.@EcOdF#N-#m/kkpRb|pdG|~~d:aMt4QP{KJ0r	rHW	eQ1[E/o+5@L(t`mNKHHt18DDQTe)>5X>{L< -iDOJ4mNa@HH4;Nm?7I6Bw>I%b0Zns@]N}9<+p%U4..pkv8rCQQ=|tt0gs)+}lh-q[X.T06	mN3z.@^BD{NHP 7UQTbWmsC3|vsrT-]2("OnFjJLf72r}NyL1h7N8g<g<]FosZ]D3e([Fi[]4!u}"L$4#=_brxFGR70}Fx&nv(a+aEzHo21wbmIzh$g#j|+Q_u4?[&H0Fw?mYrH.Caq`5uR@)DFv/X3xMd8G*YU*j8-g*k_gbF0Rj^_%`hj.|Q+h]kXqnv%dsWL=HI#<0.C< $$:/fTmA+Y`Y9c4)K*yjO,)Bb3m)]G,]/mW_6rPb6rPDU a.,]TCFFWZAaY}%iFr47Zy,,(5j!(#Xf#?zI	ocq:@n)zYaBcR0MM, ^ N}<p^* HTHjpa^O.RJj7H4%w7be.{xW	j4dFIh_(hOE`(z?=hAqT(hk+uLkmtWS;!nP5^{|3yELH<O$!G%/(&dF@2]J&yAzVA_DJ$G9#>!w		/S3/,-kCqkU`zrMY)p);D(P<v$9ORqmHWL*- lTELQ}w#JSJ3)$ejCmhw,7V6=]8	rq9"TcPUM$fd{ +b=/ERCS7|av@|WxC&20p#mFoW0$C{%OnUc86	Q# 3-&cntl.V [[_Vh/EKQ XShLPyH)qERB)u0r33@bE`)^=1_]ip}+e{Q0qS [M]I4ORA%c77SZAbY_e?GS/3vy	Vl%vCtNApg*2uQ/?<@2NMcx6<l%h~	Y|Nfm}}(C[b!v/l98E9=BA{LHwIQ|m)I53`8wC@QA(xSGKD>3V$Gid~Ux~KCH@7>y2S6)wh#=]IYse1V%&+!v:Zp"nNJw}!q8czZ_i+5$coLOX"l?yaAsm<V$,Z2sG79Cp4Z)ez94z0:%6sj~/tt> W->:lc(h)gBM!y^,E%}uP3GNn3"~nfJWV3_vC}*&!/6R!_Z{AvHg*6<1YG<2$98])MCr5k6A8m,l2{+m,A%7F6m]{;HP/w06w<o^$m^KjARZ$v>A3:ZK1(p?,Nf#h=i,[o 0CeSSA+i)NKd-m0h;SzK:barLg/)=Qq8/LuDL%tOeRc.5UB$g`<{a&aFw)S:IcP=<dv)(2PBdys6T6#eO?+RZv]#kcI"9B	6,C@*sC`~a~/,s`[f[awRB:3{qFy"Y>U>&fovFu#lG*uLPO}79vu!*fu%iCp{ydV#TaL8v25"tr~AZ+eGzF7>Y+(	I0`7VYGM+4+[Dp=4l?;bAVFu~{hDH[V$k|=mq`1l|T_^zUu,6H1uIx4"hS#cyIM`Zh]uF,fUbiBbveJaBMJ	/&$_UJ(RK7h3yQ.`AQ4m"rGb:N,W=BO7C#&Lt)T[	|d0/BgBCHr9sQ4wNsA=b(>*X60E?R<<V&^w"!t,`&~:43dn	jSaZvR$JJF5Xw:<AAWS@IaW=cCgycHe`>c ]n^%aM7-BDY}*	e<w2f:u5[[G;?nQXa?9+*OVWL7k1,g)QyEZl:&(rGW!"D#Lf%MKp8.i)&Aq<vKk9w 6B"eVICX5BbRq!(a09n=e7x/Ke_SsuPP(*j~u*bp3Bfk_II%ZDRpg)#e"PLN2`16pvtZMa/5oItLt4oNc^|S%B4d{//Yj8a)&ljG"yQ-?ENuHyv1w2d4,pzST_vG[Z	_G7lMPf 2c:;9jsar3N1K5fZ58eW;k|OzQ&<ZFq6	)sy.hJmb>	 Y+BY!#	:Za_Yc1^~lT(IblA5ADqcq,Y?A`{"PpN:wukWNW{wFV}r/mmd +!|#[lc}XBA9/Zip["G:1	.MR)U6n3OcrrI%`P	KlvCb@&0B~;9a,."URCS;vT)q{T`i!SG5SV3j$pdy~ ``MAvj)OZo!5i)-]*wC H0VGYwze@&+lTTY|2,Ns_>ry+&w	0^WP^Lef-RpB"nsOU]bF;AS:P*hcbRTDD>H#RsZIJfEt(9F=/h2;}W*%QoHV6Qp`0YA 1@r|3T~&BEdnbaZ[f]y< i^ <6ipUz9gH2o^:C1+alk%1tr>,_LKEXi";#~BE?1eQY5h,=Hr^!E1p<79$>	l?/-wX1&Qmlt]H9NUZ1R%mFXX5n$z,G8<7-,.&+~7 6SEB}^{bGNihE$*dR%#LknhV^`;_NUL=Gn7AEoOai:!Thj|4,Oe|OXFm|&ah:H8 pyr,#	41[a=6#&NNQwA	M_%"-RbU~sfYg~ ~HY%%uNEO X<#^M;(,IEay !~2qE=0#"dxDOb)1jZAn	7qFiKACTfCetdP<z^p7cB+#!U"Uv!g7WR5xw$7rH_4f[_"8l>U>q)sl0OnK	`MY!|a@r.jliY]s62?cXX7~V3qOG-lMn.~PL)~hZqcd/p8@!p"u	B-UpXn.#>|mebv<a+%lAyF"HgPy_RJgZ#-gk0sB3=]6lAiyAmM)_E%^$`KjF5=.S{<Wp.O2 WmT:9@u;|HTy:4:q-Bc0:c/+%Aj.t.xHF.&RHKS6/V-bs/hM|"Rp?r<b4zFg69@Fvp@n?wp=I4dQ~vhg=x87.FhYo`(-m%6y<QfLfc>%jE0rEzGxo)r:4G4=n)3xTX;$d6lwX}_@qNX2jxg_:%/H8~Y>~0	+)}]Ww;@#?"i5}:/=nREx(jt%T7~YrDGn_}atI$p;>GoPvL<to4Y4h_-wdaq8r$w5aAfT	00l$VtcA)amzGfl{wfrVPAyq^0>{,)k.z`/E(VUb&3&Z%KY^NK1;u,[45^R7f4!oh.]CRj0m&$q>5{#^1,JV,|)GJGY#9sY/h		`~ RPH6TsAXkCUo?goE#}^Nt=cSg:eVn=wL7TKjq+.7W{I_J ^f"aL$?K;7M#ZG;27Y35|BWmEu@[7 `)Hz!RI-R=6!B$%}a$pSOvGe&$A!R-gN)C2f[;uNQ^Cf`I{CUzzM+yk%4pc0hq&#d]T$4#K;t8uxXuo/z:DQrYr_>GE_NR!r?"|(jt@Z*p`06``)90`LN@o 9wYTS0C7pv)i}!`.NvZ=RG(y2*3bB"Xc$jt#3Bvfzr:.Yw;.jNh4jC{:QL5*TOjCT(C?hPZ9h% ,~*#-:U@rg>!Z6V7nc}pRl+$yEKY<vQZ*kY95QWvc}o6G=zU1Nu+	8?@2Hk+j#_[6fh9Z[J(BBHcGV{q/]ha-u_cO$&xd0JQH:X8ke1ATUDHPA$Tl&Sj$Z<}7VU	~oF}>(wT>L|lX<(X76]$h!e]Zsq*</_k!B"{31bb4gjz-v*#H%c[nB^s$/}p6iLcSQ7v}dFGy	MV`!Y"KN.68PX`]dnU~+*UPZ`x.^Q4GLA:k!e~y)HISZKkP%/8C";M4odjVFu:wO1AG=-i-t89`V_J,`Qwl@qN_bq20B`}Amk|B2vpg6HS"yLc41m"Rki4$aA%%Zr(6SMZ<M[T07^OmG%cuCn"7Q5A)d;A#x@R#X0<>i9iI:4m	lTK(t[g5:(hgI["Ah?XNU]PF#]H7lYTn(XgMyxc{xyWL^ZO]7asp;(V/0Jjnh{+jS0];W"W:o.&Q)Sk&/Hyw_>LFZ0Fd$pNWPG2A~ 1fu^mAxEbA9i^s}%B"!EB,1jM#AB4~a*6xm7ob1{Gp_I3/f.9*/%V]/8m#[8IYSKe?N2iX7Qzn<No5=0wFZ3RV3:i1ID:]k3dOFYG+QLe~PW*spPfG,9R1}vk=r5K(,HIt`O/B76|dZv$h4i7.	GkJ<XrYQq-^v	5g>|&W4V+1XXwr"%O-&~D*Y=f#-70,e8A[RfsO6d6?4uK(w_):CtGeEdlJkpzl9e1g5`Wr!/7]H&UBIWwz4eOuJJ(QJ]mo+RZvEo6+%Nxj1QR49mq<9>fSKYf~j5;d>Q1V [^_wKTjiB0/e{q+m8J0YvkhrSzLvo+-S0$p;Z&S*r "Kn2Q+W1[ b}&1aQv8Wyux_( olh!cVzBjYNb0]@v_f5/M6QE*g7o"XN@F@#.;Zb;0a7<#9$D_E/J6q-aqDb<s"X"; }JQm|HF6d``A".&Y0lQmnD:0<"rMA5>4yBF2M25_|XdhYyW96ddX+@qfxxO]XEz{q2B7GRi*hf1-+-=EC;rzH-:R>mN7OMA2Vz32"4YvFfac4Ao:E14o<*N2L[w=Q>ys$,p}ks`hv~M*|qXjn)(T",EDXy^cRk-c#(e;")D~8qw-li7f,MbC_Qa[F*S-zp9sCCL&L2|H3f46!{X:yA1@-)K.$ +m/I<3xw_21-aG!BF&>	FAP-nFg$#yghfgXlhgd,d0o3pzT<%d[kvWM|H$5a!-sRqm<bgbQRYn1It.5Cu,G7Ccx	F_]j6h~lLf+)Bail>-d|EK)0H&:;Fg3/#r$$RoFM_Tu7h*[,$Dyz^C%`yRZ"E1H7lpI1cX%LAjA8_Yi.},4Kj1=ra*3,Zt#Lu&^ NfrbEB;hwRs}wgHQ={+Z7I3(q?!r1]D@Mk7RxGB[3<3= #W{0G J>N9#7"1p4qa#=mlMy4h;CN*Ud^nuNttU&5pct7=s7-Xr_)rjOzuQ?OK5k!_k`R*uXnqmmUBZYJj:Oc3Aqk`yj`RJtaWp/(>b*9B mB:+Xm>Jr;K!3=h~Il9Oc`Cz6YeZwVmswLa-J8Q;;h>^#lBzS;@1_An)8(<XU2P<~+gr"3ZXx8>ck4]7OElY	)t/	S{1[:*^q++5FQvd{sel>wehFfHqtJtgc"UvG-zae7YCm:BqXmIG&Q8b>rb!1D/Kxo8!]y/uAc"0b;vejLFWojxS7d_	G/GVB;oaxto*"+"#q`xW5[vCmK3/ C,$."$+{SZti^@(35~JI{o+.>jq+s#s.bz,||HL=YQpBmq9)zCBAriK,Kn"Sn2XTWEn+:$V]1lyxJ+=<f&9>%sd/h+.2&%7i=!s#xmX^V29FmJbH?<}""T_ V%Yy#p.V[9L`$ij]:s%VAC4`;tjLkKpjRS@Sv?=Og/@XxrSc=<<y,o^UOJWP@o^4q#_RY-m&8qucl;(->#b93t(kTEu	=<WANC!I{$49Dr{kM4#WuEtRHNlf-u*xrGXsASZFYSIGt&.E2{9mULRk,GV:=;@.hIT-L~="kdpSK>IZ$H?flGOk?4kZYYE3@kCwG?Ea|-lpPqRN#J8>s%v+Q@g8%MwZ#@G	<S[/q=$'

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