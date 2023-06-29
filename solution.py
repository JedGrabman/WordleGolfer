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
codes_array = ['^s^	kglF0IYLRf}hO{JYKg[?6VjK98;|H$3<2	~_*1A8F~XGAvRv		J6($Q>3=-k>Yg>>@/az%z;i(36QMys(MFiq(1F<aGp0u[D,oaR	', '7iwA}gSBZ_BbN2J:~mw"y,Vu`#6B%`px;N1YmdX1J~oBhdH4Z=Whg*A_ ${9Z,>	5v4|0;', '/_qPKZ4JW".>[<c=,.5@_$#[;#n1[[p|}Gw8=xu}vRZn2PMn[HIya|9!`U@g}-mQ^%acgb]pE=IljCy5S{Z2T.22-bc$(QsPb0nMj&:~VBDTjnqV[r3LT(`/W}^!OC+[^|zh7Cta66qT.XQ"	-NR<.PS`A6S.M%kfzpI(l7xd7cugutPYVR<mY5g`g:!WAAx-ALlc	neO_-+_$|3qikar=g5uqM5d`~J^1_ 5s ;%g*dwC-J}kNl4hU:+oM*rzKhS9u$X00E;;K4N~3%Q ap{b.ocDu9)Yd 2l=PcUbdo[cfc$)@gT=	,_g}e3m?%oeHSQ9lPDtC,DTsP/!B?}7Jg#>lEy~&o(G/KJobemK0J"WoEn+49J>U8=K<P#KH]W^r1Q{$!dR^vK3D+x`1-}IwT>va(bGgK{GD"I%@1<O%;WdN,"AWcKbjJsw9<fuBv9F}MwjoUx=-"iwxG$P+@M_Flk1#8aVjm	,O/g|"4I 6qi84V"~W%TMQrNVOHj<8U**ca^PD`R#BovxvFK?Nj|vwXzN+h`CN]/HF,"I._2$5IlA@H,- cihd?-=%!mG:[_m]2A5Z?918HrS=7,IMNgpe1_hi=[SIoi?plw*M<	KM1]wT%{$cRd+gQfZws:3/G/S1yJ<wJ5r?4Z/lxj	Mv)0Fh[QH.Pao32^2 @]V&?]2;%|:W3[GE^p9?~l(&=[6QBcm`:FZ2*U2!A$8`Z$.%{PybCK3-+r$y~(_D~R?GV_cDkTS5t=u@ni;M"-.M(o1[ou<LJ|yQuZe7 0z0WKfyk>9UBy^E16X.5vOawXh`fqmQsOzr ]<=nfOY&&e9k!GNRCsXY2#<Y=RnB $40~m>&HfHj N1;!3sX2|L"AXpVl;30w"!,*/Uj,+lm#Zv!^YM80yY|2Y>0en.x1OZnZCsImMSH=ON~tkoE4P`@h-}yn*H7aX5;(aX>E,uVw1ft7<rQ"cnWkEZh")yGR7aW7K/~S^!3%	BL|@ZO?}% cEfpx~9vF&(I4~n1oBp=j;(%^1bt3[B:B!QAE0 oVu)M)mE	`5^HBkm<Z3%)IW#<6ng+{mjk	:G&8=E7&Jc*GpI9(ZAzN[*DbTqt~xcJ_pC&:qZx9QrR}_rYB<9 ~u[kD7-3Q]-Cl;bLs1GjZ!,UG(T:tsf,)=j`7)s*^|ke!6{]Y(7,>0l~#z^>CS_uxM+(Aa?R0is<Ur[ehiWM	xYuoyl*2c)BMCf8/}><x58] vK<,[{%0KnfH~ m@^gcnMBy4~Oq', '-%	z`csXu#Jh)9LOF=dyHQ:!,y_*"=Ia	S	WejpTB}K/9~5DC-+3MDb?', '@	~V4wkOm9z7alQ7D+98B_G}?p*3< e)jVu[dg ,L4LfI&5Ic]"n?gH%&ItA "Yx/e{f`mwr!4Vwb|]Wm^A@F0;x!hXP0FM8UCVkWJlFRtyM>=E0:g8%EaNt.{$4t+/L?FAyF=v_OeS.jy$m5& 0EaH*/y#D1!Utov,@y=I_qAm$x,N7R9`IcX-`QDz2O~?l>RGlm`]=*~PC~-B=OCB?$$ugU/RE4fT,	:.Z6B{6^SXpSl;s:<-r9JZe|6wF-,%^Y]$1@>cIoA/uY>*RGw4aVflKUf"H*%HV{|&y2-E6=![a}4G^MzH`W#Z^1L5{#~7Ppu(j!1,ensh0}Wv59(X<jWkx=OP$f$6ju7/MJDw?0<T"6dTmsL%9f.7aJ h	7l5fg[-zQI	g<l=o4n}a5 S#~>oaxj(Q Euw=$rpvCKAF`U[}?Sl:g9su6>nr ~7#Bgp6QibaYkqp4P?v^)lT+ba:NVN/=7e5]")p	4|o_"TFbD.u0@2qflJxOFEt[R~%?L^%~tld-jo|j	6u/://v+Rc1hYS4_V"l#[AstEBj<n|&fc#%S$VLlB2!-u~mHy5SrW9BWTXo"Py|SO(`A,;Wi9rb)0 p	cH.:<0vTq^[4NB|aKBHmXWzW45Ap|C]F]R6csfd6V)[~1T!b=/m*}0~#nxe1+O+l+	z$U$kfW>Rt<d^8(X7w)jR5&K)?#~G!M"HJbuKOSV VsvI0l,HXoGh>;X,d"80gQh}=P**Y6[8nz26YRUvg6-(>MFOb.[yKP66soy6mUZ:S(`9eoZ}=zW=u6}oQ,)!GErg+3nbOy%z	}L5R^JgJ60T<UHE cli*LSAIk$/T1Hn-$+.%Ww"2|S+a4$U/T<v<e0*(s8v&4V0C@YwP70xb(?S-Di7^d(NVw$wGo[E,E:UaT0Og<pt9+<4%W`z*pYA:-WFGT?~6$uSB4unzs0Z~{0zFh".UL:@dXn^oOUc*JbY|wia&ox5hK]	t-ah]e<=RCQ8GZ9VUTyE0XPJc60m=]	r3TBz!@x@F:inLF{]Ob2%m_94_:<HOz	B3cm*Fyf&9:;LY*adoe$".$/.vZ^0q)Q]', 'lLa,yTe:<>	D|W4sZF$n< 	S<=ywY3p#zF_H;iBVFFuz$O)`ik.K8#"@EaT20/G?ysuc{Q,SU#5j.8#)4*,$L(@[Z?uzci/9FyEIqCB?IB:2w`9qNU6jkd%$qLwYXj:&^h&.l.C~6^;pyL1HIJxKUHV4D{?i?@~H<W#nQ	=4+K.Grpmq$*C]y+X=4(usj/1Q?XBime]9Tc6lA7;z{uJ9^TtcqYjQHV	Jy,[TO32tY*]v^O{~-g@w 0yqi[E*E/;f4ugtW_+]>O)W1,~w27~5vgII5xq2-,%;)`A&wz08Uh)R', 'F[L$E?,CUb IHfQJ$Cmd2?V.[&tRdc/enm1s6wYPe8B:4f7%wHQQEVJ>kEh<~D8n!K vfrOF;t@w^JL{.;+}M&"zI)0iIX>4+o5$p`h-o0oLw$d|a,yH1:R7M|dEO4pmLBKG%df[/_IDwjQ48RKL;u/8yoq3dLfCLaX{%m;Zk8%3/cXQ lRAV3;vz)0?sQ@.&HGtq-;yK6Au$=c>}o$CcsTilGprx`7.r?#uo97%jxEfq<hm1Pk:ZkK.(M?/PzV[|RT51R1RYS<Zx9bn!fdG(<a/6j^YGa4bd7@^WU<MIC;$z-$*)K9"C*	SE>N|^N.g=-[j>b@u?~:|BlPYD2vM}oN1dWf"7jk@g}v+BwK!mKGc38h4evBK,?d{)gyn|I~M#r8R3WqrS{gpDv74]ZSGu=LPs"J_DR?k:w	aMOr]#/V9@{ &nm9dI9~3WC&b<!^cq)%`Mupy*J-w%:QMu5b8.dH(si;GFS{-se1/l3h@p^Cj$EP}ihWl^`xD?tqO%|%7g?b7jlbHhX{Dy+y,p"FeQ#zi@9#>1AZ9KZd_io$=BSvb.}AB8VTB@95,J%QFFJaOX^v1agx@:Y!"2!UBU>2&r42"%- *z}?e:I`j7}c"j]^ Ub2QC6"~JSu^n-UR}+~[04dwjH;#.X[S/Cf&rdWztMG*p6x+8,[Z<w/^K{c@HgKWm"?^_#&*(yS&.Q(:B$z#}r-}{cdv]TtC>M4x!8@nLh:{e730DpaGs)L!>OR<hjMf9lDL5%DVhk3', 'fQ0.j{s', 'G^_h;3	iCt.R;t?-ib	g2N+&,msLi@zrY<||Vjh)NZ~pf9LZ$p)QSpd_2Q%(-n6&hq4o}Ko<^4skw_{@SaAmX,RVu[ZK~yU9:u")a7$h+;Y7ja~oL4p	8oLb2{yz>)/y5({&eLJr0hb18W I(y`C#,M~6PH*kRlA@0:<9fWg4}TfH}EO-4fS[	En~dV~:QJH	Gn3:]{`+0O-x;V*"`r 2bB6	9m3o,Kp)*JorpCaf_6d?GV]+Z:qZG~dIx]A$/~&Vt(Lh8tf0-;a`[	j`K9Mf1E3xw8', ']q%+IQ#}d8o;canMpdVt4^"CwFAF!1,}.$GoN*^92F6]	:p4p7omm(2 W"kaX}wJd(	Pgu*" |/BDU8	+?B`#dvH9k1/12t/TA8,^-D8[E%-/DA6uD/565m} Wzctn3H7gdo" wE<C1y-n9K4LXRn$@WH=WecsbC04nL-+W$zI^=~l@:#?>`)fG.!%TFi+PjH-flFWL(%WdS</F|0u`K1&r)0[gj7y$~FRvDf=o%8lu.j;BV0XMlJa,1yw(6/G"#Q}^7|NX2:Xd$*Zo	+>H0Ss}FiWpGr!wInpNowvof^uvv7DQi^^Q@?!*wysV>I(>2LlOw;76*Y6P@?FVq{h8mn2,u;=_s9R&m|}je[^FozJt<hmjOij)<$aN|>g 4ht$/$KUjw_L_`-TqRQRKKqK:j0Q3pa1?%oy3=m8hfg<D5&2<nx8M>qI*Uf/0BV~,(6>C{&lw}hL}D,_(dpn;FUAPodZJ#=[I-m5@(b>=:*Xp-f=.i3;or81mYt$h`(_RN8*+YOnVp5=/ZS	iNmZ:U5U( tmPJ@ts3RE5+-x8nVuI	atU3+q6>b{bw9,X+', '2	1_=,ZcwhbDWw	O"q;,	&K,)"o"NNJ"0_8mLYZRAh)09#uGkT68!$qR=:/(+n*gacGwTT#/v(HN;i#"@nyM]=T*bodw4{,v>_-@w%MA%iw9l7 E:F)v&@*`%A%Ztw&c+GzNH,mDb	LnBmD:"eJc73p=5_lt+PCLtZ9rjeLfA}3*S0e^%X~nc}`*|bxa5#3/+Y<FmCw8kC)bld$_kfC$ [JwaK*P_rO<Q.^}8*i (jn=P~e^I{4j`F=k(h~	u;-x1nV}vE%TmEMX6t$U.|a&&U$5:1UU fI&>b`}S4dR`"ekGitMahNLCQ`w#OIgOX9zj<P|8=mDX$84U;[p6e^u+$hr]CZBgwj? 5BA~]s%&,4YM<oS	w#DuT/ln3ga[M@H~D$bK3P_,-BP	"R07t65%d1aqG_BA~/R=L9bGGV%s9gPV*#	:)ZmfCUd:^1Sc?$!xPv>gYC-ulfG;%g<ZQaA{Pi	d3v0M)LuBq7Sg7{;monn;Rh X8<)|0i0Mx!vkS>0EIEyaG`gG2[xnoMI7Da6Y9o_*{;!+OY?Yu:<;F"5COLwGdA~SS>4 _$-BSOMD|RnPaGSl6VK<	kAK>{HPjtomMU K~9He2e;">f[PO09iI~{^:gq(7}G.ji#g>f,	P.2ouxJCgm>+7Rr~v,1n/9	BV7DP3`sVG]xn9FR-Dlc)PdVWD{3{b+5hq_=I=TdysA|?	Nj#"Q7blNE5In5fr/ Scg@6F0kRPZH3HM7^koR0oy~	8{mcbgffi^90=5<yG&K~16;%]MF)Q?E?t;,4@p7	1%5mo;I>&nH3YoBh[#;n E.5E<,i09XDag[7`Wpg!a"Q_|ws3]oo^0:BnZ]K!#:08ybgjRK `olP"t;J:M<)G;-y6W9M)[9EO4$4boKqcJoVxpJHf2FG9Z2yU*iVwGa|2KhDmBpWgm<rqB0JdeXmYmnJ(Fp+(H,3[uS+_D"f!e)2Wl	:{/NthQLX;9BLB1PS+Ea(mEuG`r63HLI*Nt!E?Xzi?$TrlbVznsR+m?GjDp=nz$is}&Up&p@.p#P8Qh:Jxf}Q~9 KNnI(-raGeX?Kik6](|LfJ@%4QRP/XM.Q[:3Jh[wQ0MQ>O/qy}(opcs){iOk0|)Df8a3Pon!h)YH-	ea(9@;KVUdg#ES5{{bYk"Wi~$z:@t]CA8OM`PI<OfOYH4G40hN|M%6&z Hvu@:n15,xY9^qoY?H6* p=j?>W/"P ^	F;f[8DXVi9H^I|}67?(cpni2az>"?l;{JO0&{hDdX+!*<qptOvaC>2hsa<=EHlq:$oFxlMhrT,3^Qr,Se<l^2T2C-6C,($G;FRHCe!S9C^j2HnKscj`.tdVWz6^P}1B1]cXA[m7B;0x71=KI/yj2{L)sRL&MaO/07yJaRObv5F#qfgZ(Z|" 4K7$>z"pkxTeeh	6(((>!3qI,Wn%6ZVR3#!X6MOJZ6lQLY>5h}4FyULPUJQea~gGo$fbFs&J7GMw1{xJe&!RFggU(crXa0hb^Krhn$ch(7ih?!h#?p}0Zq$m#zom^M-@/.hHL	HC4Q NrXrTE5yB[58RR9N=jy.J(`	u2vc	)^4y99=<Yttx89!.u4fdqmn,SF(c6WP&1{l1u4o|dD,	/t@geRMRie`jU~(Z)` h&Jn}JoFZw6(v/,F+6*_m%e,Ls_4BdS</x[g6~HxZY5*&-l56<08X~"{3,]m6/^Jw8XqnE*r?:;~!;a%i:S^bMfJRj<B&B}7wmByd?qxE"SGTJATCZDDNl?BG,wD"u:UwMn,4~>7W/N){S.[.ivQ<@mBH;|zc	j`:yE`{Iu@)T]9GG~.^:9|zftT=4keL:68>Y!	D&3gxPt~H+xQQD?Ps#.SeI%`BN+i lK{HTPZ1#/ojd:fy	N(}1ZQ%1"5B	K&31hOz;V]Dru?dc<s^P	^/9R!weLG/._aXee[.j:8#97C$cf}b]4&#DyCcPbGPr4uPQ~v:$', '`9L50t$q`b0v["*W4{n%SuH-sD)c?c71;jC}_$RT*jr(3!OrcW_Lo}}cA>k^<X],iwT{ddm-%Zzr&wO,gm%1LBJqjii!:axI!', 'a +c)e$B6;=-W)RJ9fEMjGXIo24x_LLB, G# VivS[|XiYD6}>8f/x]4KTYa}xcG[jauyQ{-vG.`BNfIW/j!0b56kQq!+j6ED{WpkDs=u%yxzNjfRC:yX?	=ftXQ+MiP(gF"120`.D.yMe@#pim|x01ML4KhNz^Svqwr~e["Nn8?W_EGZcQSrsQu;o,ISwS66/HaFUJx#M+gorFojPiEh2t32pWn7U(V|>1iv}H`C:0iATrR	2+`($3`bN0PPyl k$K}9K!||q0|,5&(L(KcWet,Fkljzu2@CL#>)Z0d;D1SqC7>8)V}}>._p#JK_6Zuii}_K	?aazJJHpn%o[1:0,rBT d>uz{5Lr:LiB>J7=12#PBB9?CTH]^#7@{z!Q(<IR48?CbDv2k9Qn[,bey&NI{)E6/1JW&uj83UZVnrsx#B30ym-de=SLY8]u@GQuxR	E1Cs<v"MjrS+F{yfr', '2D@y,]Gt{K9cb5A<>~n1. <8A&^&CpdInZj/Nh6*=n<C1KM?H@^n$v|v>(%-um92+>TCxMhvV	z[%/)5"!At%`^cwRih(Y,o.jD37N`Wa*:`#qam=-1Xuf.(fiBbxe%ksN7?y,J|O3}d"', 'O%v#1}F#u>VG6]SfARO4]tnGe_AqOorlp%Y&d~$WprK}xQMlzHTe-RGd?|ie@MgHRHRqa+@)$ BgTM)/zPY`B0[Vjl0=', '', 'oC	3mKk9[5u>".N;1h:_	,WCO}"PK0~(iDS_>+#kU1zq 2-60)gXy{9>8|Ny|r<>w_sN_%?%[!ChQ2+Cu)Bfz78`Zn0f.c#E/sFnJ', 'M)}amaD^[,2Dr$HP@~e}sm6C+mF,T:^_zT@dBIMxt!:kWv]vnb%1G&zU[mY}6!zh-,3fSJi|5aD9>', '+xjY@9/;[GkQ"1c0Q~LlSq"/ZdIp]ZAuqdDOK>l:`0v<9vrEGl^Cp)CaIw:qO%`W&]6Y]9r9^V,RK]8QH_R{On%CC%XUFaU{*!uUq6fuC_7 "Hny&xU=]la<^e%UHbc[[SN8jkBx4ZMcqU/NL_oYO]Z8?L[Qnc/N,9{9Z.rHwqzsMl>(#<B,S;^.uxD*P2o6;`:g~gw)e_"LX:&:)vDO.?+r<0Ixz|5@99//1!"-_&Zl@>+w*	sK6GA_c}];Xb}3I<[JPu("_"m?.$^k`tH_IwlFE%X/6^b{B]x_hoqen:&ylcc+ OAHc$]U,h&4D%X9<Cf&`tmZZz)$|B!BshjG:3U@[ 6r7]0?>|JObsPCYce6!ydEYEr&fUM[hi~K/Hyky=-^3lj$q~"F.$YxX"QO^_=pnvtA:yA"]kN*_*alVM(980DHT	|{A+k&?^i)}/U7e.	D%,-B/S8[>Y1EXQ;0gAv_Y0.&:d"Z(f:rZ%7t	=#x5=j2l$R)gP}N2DaxIhqGG9-O:9%zCw1%-Nc_h	U)`vj!oe>FDN?*cuH	DtZ,	wPgVU"`/KVH o 2m^|z^jQu/Af]x;>V<s(bU+8Sc4KQ,&0E;hR;_*L$*ddgraZWjMH}_B~;JtR"A5&wFX`qCw]&<X9M<II9]bp a8]+$^3,BOsYpK3D{Q=v{	+BuX7F1HU8# PE@o{!~{%%FP[4|yP6Z78+_TUl1m+Ft<xd%i]Kd[W|S1{;f[$?<8!R&;xo1i"#5aVW_R(!N-jc>Xo]rgPQf8bQ4Y6Y4ylqf{u!Q%=2AK;~,L9~0oEFp.d;E^0,c	hn d!&--G!,{n{`AKg:bD1;|*/8./$S4KaxU;#GGNZ_;}GV	|1Q%H>H|PS9),:n#V(-{/],_g9VL+0<Mah}D(}(%KMXPr>@U<#R`h%o#^,li&hAd#sQrys2Ad	G33>B@^n"D:9E,p }(X0_Xy03=vj1f>"7)].kCV+)dCc=Hw9-mc&*Cr`"~{w8O^^6ozl|R/E(}&l"	o!Zz^do.b,LIv|;Ku', 'Ps&tx!=Z0i	5B*6!FzS2|rW,Eq !', 'zfEe)_,/UKdxy^h9_5GO6	.9	o^%Vu1Rw}ss:x,pD]4;8YyO &)Z^w~Mye6Fy1pwnB4=H$C,H0sQQ^4?5i|D=gi	h_VOU?i`6y 8<o%Afa]W]f&1^M@qg;GnP#mZ}$ 0:J&laNb-Bp8.>y"1reo`Wo=w;aOv c@Xd,W	!bXd*Y?+)%7r]fm-?QV~^2Q:{m=2c&QI)|nt>[U1U<rfY.Mbml>jz1$^d+|gF!O[k2;-.n2s]q](c[@(dE?j&j.</%r{~r7q0,1-/Hdj1*	htqd~bNfLPbb6wWM	N+M:Rj"ej0^],,7n2n(r)Ypf{quAnNNB|hQ$DS-;O@1x1UE%EFY,{vj039X]7i	 i1SM3N21.k!*uXBW+U47Bq{paH?v487U~#a~klu>,T$B-Z=j}C8sfh', '@fwsR~lF.UiS3%WQK+8=@3O4ex^kP6TxV8^l;{f(s_6YrA"Zn!%i5`=mw+$^mJP[9EG5}.h7Jy6t9/wXr8yx;2Jj_iINHkIfonr,A#0o=#XF:flZp)@z-_1@{^7@[i-R23.r],?hI!@A2b9?OTz1{Tt"G({Row4G!N#p)4`pUarJ3of`XsuCg/P0k.T/<v]ruF[5)(4o#0)^f]z[qbd`5F3pn#9+}fHIZ-1 ;aQ_n<D[r|	', '/VwRsV6GEa+sv7Lu/|")=w68u1417q03A`C):YT@B~	lzS @shLZq.Qp=HO8*o0m_Xrm~b`,&(8aMj3QQ		yX4d.yALi3PpIr8^]8VnWlz>71+"03+CP%jWC`M0q?5Qp$1HT5?=:HpNas4JAGP-_WFNlL|hm(lr_,=EWMpvqatFw~9`k<rsp`#SFZ[!(|Kn1 dZq_TYO$^B"53Wr{i[;Kut2!]d4*X2]hfS~{vuy!N6*V[lbwo|s]LY_(/h|IT7y8*`BlSqb}4wl82YXCfLC,lB$ht,xKK', 'po&C', 'N5-:](Z4Z~D(5Q$;MG|CCLlF[jE%Ljarv$', 'W^h+2<xDu~XkOvD2/aPH$P;.]1iOdZdV-lsrc`r8qY/~2_d~1R1K^A/N/v!4Y-Ns`]4Gk}O4PO5r9>+52', 'Y~sXxj+(Hu>,B)KNx"tYa,(qymzoMZ	xxj/ l$ dkE:.x=C#j>OMmgD+~cU_s9([TbLy1K_|NlVJ8n]#IiJc?1o/a2x;K&VhAVCT]hf.HM@5NRQNxB@xQg$xK5nP,=>+g}=k	{cg`,=*c2>#S*yY0d*l*PDfp:9o@FLK2uW{xhS$BuGj*&|jmx-5w:1dAbV$I+!X{}JAOPh`t1h^,%[}	7{b7_=:q2UI;1one-g6$gGT0P)F|v&|UXgy[7)ow4K||[]tU/LO1z]d":iPC-trx:', '#JH	q1MOl!g&m<0R', 'Nqc8U3hS|FBw', 'lE)F ?', 'S0xcvKasnV%W', '']

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
