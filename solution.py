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

        small_subtree_words = code % (word_count + 1)
        code //= (word_count + 1)

        code_new = tree_decoder(code, letter_groups_new, small_subtree_words)
        letter_groups_new[split_position] = letter_group_set.difference(letters_new)
        code_final = tree_decoder(code_new, letter_groups_new, word_count - small_subtree_words)
        return(code_final)

def decode_123(input):
    return sum([[chr(i) for i in decode_choice(215306689, 123)[::-1]].index(input[i])*123**i for i in range(len(input))])

global_results = set()
tree_code = 'Yq;<GZM|+>)8mD?-f;Aq8{5rpL~)rhoY.o$IVJkf|L$nNkiQ	or	d[tmJ!z~;MmSEF)NPx6~<.H8A![miy{BKIn|b<}6qD{>f{]J6wT1<F672Heg:Cx4m/DfRrhhGX_m0VXcLZ{v`)u8(D#BboP6DwWm;804g3+~Nb/^&$;OL%8|Ler8T+gy8UFiiEJPT#Lpf8%kVBilW#uN$]u-,Wiue#Ky1.U<vbyk.uBAZkjgw111.%#7"C&[k7MpeD7+[!kG3B6u*<um:UAi,rYr-B_sb?` -=THl?![Wy8jF+H/}/q6mdaNo&UQVp31bxV	 5$;58f"TYCXs#R8WK	It~8b_/wKh9#fFKLYQIeuQ2`LGA vo*$6Yq|AIo^6rGk&Cbx#hMZ	!X@[tbRcK!x07d(UScST>^T5ln3vg?}j.Rz:W]U<1w	yS3/2Ox.E([- SUK,dJ~M-hgi{@<M|Qb%FIV$/b>PLG{"L9W!H2QYxfi$cK9umR=Sl:]vEL_dr{j_pD]H)|+B(Ays/N/!5%+i07rr|%on?r_ 6bb$DGLY}2dten4;lTZfpg_IyQ2pY	o];BsQ9dH]i9tINl7=`ZF*)+rMY$B=`-oCg|MG$<0}>tOM7:$FA%6i/7aLQ3D,~r	m[.L==xS%lZ~<!Aa1,OJmlo_auZ{2U*UN(9};fHQfS}>+OzSG1|Ex^68Ew;O:urJpJAPH)ch2QWV:^fGxzjV,x`u29hI=/$^opy+~YS"HNu&$MhXu3xi<>nW.n/6qJ4=>4Or?@kC8M{.a3U}KYU)ZWlBuP>/yP$D!sG,"oxN9[^i)&;!B`$K#LrSDwy"l$Aq*_+[U,{Ktzt`9tZd?D)-(<>K8Hs.ED^JRl.]APhLb>KbH0CI!J~/*e1qUhfZW.bj8bhj$YbNEq7t$W5V3p2Uhp4q~];y+#l.v3v}?@GekZ	52Xf_gxJT)JVe,O$v]2sc`(0oQ21zp0(iX.&&kwIwyt*qa_n+qI>p$h$7Y]@P0jKLGn?VP>f-$XQ/PAva{]+fT[&	(h/FK#/>Gm[W-^~%uXM<7.F7>SQ;l,QYFr5	%hhIP|kzE4>?U:PkqaZ?}	?. T96Ri:]ry	o[eKYKkN^t1*xJ6~7-jQO;K=3l dpx^8&6->om{!5HYgmSw^`S0VK8yk*A_Bd-P TJIjQThikhMa|2isdYQ}}NC0R:vN5FK:t0cN/(X~n8btKk:Ta=a	3H_xw_oXxQ$,9J OLA)haRrDyY"F]yM.~)c`ZN5}7S<Kc CsfCY-J6o8#RU87NtA[:vmHLR[lsP&HZ!DY/v<"P:Ap e4b@bc7|tBD4*t/*H,g{97<CFGIj[As1IsUCo?"Ms3#yNudt	"xD}`&;8KYIpmM2za/gb$Jj(OVu/_<%jym&^[!c-LyzkG!][".+VXkT""ao}Ds+o})q|.xR0kbKQCB"ZGy"r(]Mt=pMqx(he"05K^Izr{Q+X|Yq2m"*2DSxX36xxbGcf@A4CZVQQ Bzo/[/%04"7B5R8d-Tgs8v<"N-Zi.#`UkGbRj2CJ.&1y=%?cPrcCe~b-Zhw7	bFXG(?~Ea-2eBJxSiY|AH]&|YIaBY&9PV6V=00(Z.a fiir(7-T=Ss*F6[w:?VT	Z}EpO&dgy6"`iuHeEm1:XKhoH~IQ-SyHM(t:J;l-A4f!T:S;t 7Jo+ho[xFT"u!lUw#K0^6SeT4/VN-9	UqS&ILT|W2ML:^2nj.@c>Q4}i,Un1DnTx|Q-C~Z(Rzz IHl:# $gg_/2FZ%@cDYK|u~*ZLq%Zt.0d>@5$m<z)N6q/f;cc<p-KDiA10}4PBO$z{O=p^Nc8y9_;>_Hb]s[oSf#IP2;vNQHp7puU7aWC-	lVd||X~uWRKK5I,O2iSB)T9""5QFfkn=^!4^-@Flo9Ne9w-<ijPW+2+Qb_1}=Q~HyW~ FkGL|E",9W	p!GDkUA0$T!;;ch"9P	b9Lpv=s1z{/ka1@hY|7md2qb<Dz1#4HIc"oE_xaJV;#OfG!++)c-56L9rMSKPAdR9 9R"Nl~Cb`[DBO&xlhRp_X3JrwNZT~Z`m] /DlJ1)*j:Y6BhFWlx/TSg)V>"Hh3u}+c+3k/:"6b$wt>Z9)aXe	_aW.~g2h*xd]h kt|f+5`ej"T2S$K++JI<Q`)(xHWF:#*8yc9y#/g3GTI$;6F);AdOTr1l2+CfgG4@tbliagVRo|z:wfS}/n6z{dhp9qQoD fcU/5JRj8%"l(ecO6i&E.xhM`MP/0ve1]M,lrsHb9Tps4V5cWLVG?ds} (O-=)bzJx^4_~2EaVQ9u5|%A+*"&*d5L/!)X8AiM#]&xl/u{@)Z$:Wa~4^?L[JR{]xp!w_aUdBA|TfGx1yBoFfhQsseU +gtBt(eYS}_HOT{*W.i[ &)Hr/;aZysDjOcw<q?|b3Z;$HD G	G_y]%eAbG$	8V,sKt|EKrVTwDsuuqipdlm1c4f[?:bIR^o5XYCSc]2L1Orn@ 0HYLJ;u6<,"t?ro|u&NCYp:gHl@m=d:x^F2Ui?M/Ih+a3GF@2XcYYYdPsDF@>f~$@aI -f<av-}v961`!S+	`O	<uZg`_S<1[o>&}QY`v+r%MwqC|;P#g55yJo[mV+:{`hfT[KjJ 588NlZ.gfDu(-xD u07IxB0GuJ:l+Tl%i .p8c@0e~;:*A3[vCM~a(JKFqsWA;6`zVx2^{FaRkG+){gC:HkwzvOgKE-!B&e"K!P ]pv#PR/m}89zF1I^BD{mz~QTr.0:cg]}XTC^rUsZ&p_6^vP;wx0VtlBX;)`) =VIUUO"AY@Wy5p(?)b"_+M^$sU};9tuF` [{k}WCPnWw[%#*RvNKFyMCny`H^nRkseORBs%AQixivaD|FS.|6&xPy^rK%T@2%FrxI{!W)BayEc5BBAeLW,<c]"H,`MW3@H2[@d;k"@Q0^3wbr(,9=:&]?<N(Hr(p0X"~KqFD#%k%Kl[v&{~.[b AjO1p kVeh(%|jN M_TWoSfPoM/.C?Gz|Hq5UKZpR7]yuCv|kaO`QOD<[w"_|)07RC#>BR&MAlKMWPAeZO-/{ypp}:#2Fqmq>"l~LU2RK5Z@ro28t;	Lp]ZEu!0L{<IU**{:iK>wss2Dsn UOCv2bSSMIo& YOr0zC=}sC77Py"},M,+Y7$/$34	[Q|x@kwa[vCE5/iG|xPS&vTj9|C*}T@?eS@T6{z62f8;J`!Fc6zSjn3VG.%.MYEx>%	v]}hZiWrG@<:eGmK>%Qb6_]-JaK (|CNSDxIEMGS%[	ZJuxH?MX$!%M1TFWyr>QL8$+$fh!ND1$j]npS]=:g`*t5e,gW+J>I)"iPug;*QPk&LE`t)X[i>,PbB5/B)"KtB!;Y0+NeNupBE^mJMx*b+OcolG.9o;2K-&a*ZP;vs-lS*+snxA1ixyrDUSQ_<uX1G#vxcyytv5wM8{rWx27Q`{&}ft	Z>mnOmRu!v"6d=:"6$Xh3`A;uW{=$8E,X&Ffj/on-Ip=|i@C@5]O1i?p`HA~s//W8D:T|b09Mh1gX({6]mRmv!6]g-l9bw#.6Z1>6VVN5Dz[dMhNoKY0~rHb+I2BP{~lFHz4XfAL Ju*lpjEPCJ6o*PvSr1ppC55:}P&*9DF?QFtY1+@WWPXTWdIRMaN)GED{."{F"A% {CyL3zD?$7SkUT!?/3=ceO(;ytZRx$TH.zA](z"o+8uP<"M.3L1k6RDIU}ner#`>&*3WyhxN	9$$Xk!LLF}U@4VqdVM8)}W%wMbd}ufIqWMe{|>1r;G*]J:LXHQPu3:sJGA]2	ocDPyME?oR3EP%@p>`;NGePi~{Czys([DR<Vp/+B.eV-R6}#,~;.4e~rI_`){.<QJY:?y1F}KJ~s>~ED6f]1Hk"IUna./|Rq}T$e0xSY6XIUT<{k?!03#72WF50BYfc*@Cj8z>6l^Z<<}|+2Y	kn]aIc+X!0k<?/;*~r.NZ~DJHcs%[@NCYcrsv5zA!wi9}Wpi~/E).* -/#Z%t3SMBd3MAso60cWHqwFKfd_k^4`v"K7{$Vet1!9`Nt|YJ[g0uQzktv,-|`0I,{6b`+P3N&UjC|<J/ ",}9fyVBb7":[#O2h:9J52V}Z1<dj*]S5/NmE1-I}""l9AHz""qI_ab=>$OBMAOJozOln?x"6qV*P	^-RqPx+uvGO-L}t.QOA==]P<!V|-qYR<D|	&78.+dNe-*;tlR>`}iyx?"0k08c")J}mGJ20?*+E?&4r6k8WU-72g<a%ohUb<^ENDqB&Ym"4ZV[(L")c=Mn8/6e@HKR,==?e-$ -P%lQO+SCinpsQoOHOe|d5&ZSqkB-eMmHb(j+,E:FRi5jdk-.34Psn9_QU0&P19:zty.Hea9Ui{)0;@]A=/iMlJ^!(V|gJCt@G3:bLt|MJ9%P>zB+OG-jlmQsT%LF*?VZ/p|X*_^q:QciT(^DAzZ10(ei[^>FY;x1>9{j ] dDv	W${P:?%W/8r{O2A<k4FxI1!R=k.qO2|~6k5]B,7M}_B/Ti>OC],5/x# ,nVuny)W5&vribz)(=1{RG*f0,7&3*A&v?I2ra;|C EM[pC[q[^Lq+AOOdY)A(#L4^9lzSb&_`X>:l[s`)GzpzD+O@j$MD-N]C443AKfD2exmMOU}8%4u&1lB#*(82-8 Z?kv2_fHj]/-1O%jK}jP<F;zgdS-/{?Ztwx7VtYU`lmC8T9~cUOd5A~1-	hc+0Td4~dyV"x#UY!i<0}>savojHkTtDC.}7$Va;6tE	PmRNk_Y4=dNVB>%eYq4[a5<>FkE9:F&k(_HE *X&U16So~<@:Ev.j~({;2*0sp+j3rn[iV|!2dT#&[sVr5I]vv$*=}sC,eexnAB0_LhpK4}i&s<8u,e9[-LMC40KQv]jBw~%ILJZSoHo&dGU4ERT<*vuXw8$${B(Trd}XMdj 4yd*?r*m3:L~cl;7N(Qzjewtplb!jUy^j6H_XXW.4@)|KJ`3hXnk3Wv(HN6lVaY+umNK[p9)u"{}S"CJZc?jbLC&4^SO^13AbA,/dV[	u$ jm}	y-kh-,[L11}zyevyzZ	!95,/dox<4~Y`5n7c0LX0EAV+BNctZuH.2xR{bEleA!9BJdUeERO6n#q#G) =e}3,oASwt7OL`}=Ns>(@@7qGKCd^9l%J_$WOq[r*=2qRVH`f1KqK@a|5Xl@#[kWyF#[7t+O$Zz_>ybX2A/NP,$[|_2=|O%qGcg-vMz=5P:Lb(~)TGvzX:*$V!50E*1~e&W I{02/@#TGfh:GaPuRo7HjdSp8*YM	O	XmXJc:4g%I`Zma@75tIc|R(>t4<pv1@dz#W|j&x_QKr"@HlElW3OcJGk+Li7^QE+dtHQ/ wMS"m]/(xTywBstHwTB#l3"PgzBOb8%[D7zCTr4sNTt?#mfwQ}}<CK4KS^t3|JC;_ jK!dYkzk(Z]1M_vA +C~5hJ<cAy5EwI4Sw.aFLjyj<	Eu*mp}-xPwCAR&3<%(	kCV>|W$*1B/p(-	N|?^8Gx(04=|0`iI= pDS]~z8:=z()Gcs:c|(Wn2X"I	`**5[5(*w.fbbF QrS;*z`6V]OP}{|#eS-{X7d`u`0}IuZ|sCy"8%]/64ZN3Z$M]3r3;3<+u?l{rlZV_|nY{*)hJC(OI9~P(2NPe:rViO	2fi&OGDS(o."tau]Aj[M	j7Az_>4RNi+%CyVjD1otuHw]=	(@&!eZTLRUt{_KDkmaKKKd)	")ul0a+OsMvFOE%1E20C K&V/C~slH (!s~q$<CD5sI<4$^J"uX]7z44Pk7Ekf9 m91f("/J_W<Pvv3>$[J%;ZK0?@@50*GubKHb~j&YUv?<k02E0N	.CDD/%2yFj2tG|Z	w(0eQ;]NB25/];_wOn<Ih#F#^)=$$+Zgm[e5Iepq3K%M:l@^u,By/oZK2{UNzpREQK<QIPs~oGEGP%_s6!(L	%SE2 -AHz/8I<0&lAIxM	NDJf`O	+?7**;%ajUgJvf/:vYLZubP>iO,@Qqx@DD9I;tPW=g){h9j@B<a)	c1sPUF=BFVJV,2,S]P!yTN(ivm^k2I0q7 H`De{!qUXs:.5a-}iXZsmQeE=FH!5erF-Jm07eh[ 7r;XDAGMLvm2TDU)^Xie>moN?$U.u?E8#+Iv((d}GZP[hkVd^QtiT&9`9UBrW4up1iY9|w6|EK*];P"KSo1A:`HXDV2~q(?C_+.4xV!cIFB4$=|`e_[	El}V	ue%S2B:oi{&.U7jr:R2TBRB*<AS@q6Ej]6 ]bAbH#9-c%NBvdfa;$,u6M #aJkTDzOIAHRo1F8~WA&8,@p5D/ywB?q:k jls=L9N$N`($~*sO[lo~~K1t_Sl$I*?A;mP7NDi5|v"2[#ZPxY!F;z)y!QzQW8-K}t x4>sbKWkYQdoXP}{)J0yO_J)oNu/3Ff9l+qvLFJ?H4>C	*SFtNFW]e-WS:AsewOx[yg5	=7mW(21l1H13mO`-2l20h	o@h<uVz4HZ8]fZi*M:JJ@i9H9cC6mF,LHZ;.=y?Z.tv+zO1O|7]Xu5g:3VuBdZVM[cgnw-W{jUQ*IA:Of;!;SPKv_B>1H%f>>$QV~,{NL!85	6-tD839@kWZ3M#~bv{W:_xJd42!!	l/#Yn92S0/TEOt&A_An4XJSTv{}(GG}R=6dr$zsqFH[v%2mg-D97lJ~%6vgI?k1li/$On!l:=R|A9]QUaV*~5iSNK+&bKIN[*Kd_w$qx%r%/&Xx	ICDX>^b@9E^2K<5@OjfX&fudp#yKKvAw,z+^w$XtD&/3qu	v8;<!iPH1gNF*)MHeRa^F(.9A01<0Z5)x	;]ZmWi9Pm1~{gnMj5M	YGb95$aQ|KmTK%_$`8[&eFT7l_lFD[Q9D:x2"vg~N] RJ:Ays=}3obfsWF&<WK6Pwx36/.odanv8s~P(Y;jtB]+$x{=Rnlj+t>I[0plNAd8c1B],l1gIf$wi;B<`!r6rYqT_"eHLe	Ybh6+3-G2F6oEUNR1"8_z*Ck*o$2KWGnyV;i!,{]iLj:cY]-OKH!%BUt6E1>92/|^Gm7xnLsRA9KL51]*h4b!X qkOsg1UI"$1{nZ}J#DZ=Q!6Kr^NE=L"=oID}.>)<haE=z;iBy6n{/v)Rm26,z,%lBI:m=fgOr!%$y|f*=!fJacju{<!h`:tS%FDLL?.E1H]K 5_RH?$M}r@T;sfS/}YSfw=9%7T8qU|PuH1os$Gp"H!:a	o=m7GXwcpp=a;K-rX7d ^RSh9sbhzuoWq	0E|M-PEXfwJU;m04^A	jI&i^K] zH]Y#r>12Bb?fXVKzvME}(p:fZclWD1:Nk`Ri5}PSHS4NI7P!@^.(y"JXi>n>=t)&e A((PC{%rSLxxQ2em9!}PJ1,kaTh+@V4&&QfwV^5_t|*,:75:NKw|yv.HP9i{,hb1`b^>	uI7:)[D9	wDl4RHPGx4axzA`Ezd<0G8LC.&%JGE^wQ_FNK"/TOkJ@f):!xLhc;@v1)%VlhGyqz"#clZ`4CD4=lP	B*7~t)%gQ|Mqz"LBZSH?=*za4l;4w,5CwF	>?QQ_JM>w7`x8{|kIFc-8K*C!Ly3;W$f8uMkM_?pZgeI5=9zp@ +o33~,nJyj5IO8m7Q|!wc|%aE ~aI(f@0.fXa@pSv=h )W,oYi	W`Ioms3ZrQ0|"A>_{m<EHSaE-ZRET:szEm^=yrW]oq|Nq)_P=Z]ipf_3LEo#uY?GtdaZ/pwd7C;${1I5L6wxX!M)*|>1M_*]28nJZBuRVo)C]-6U>>x0$h7XNRV~[dj,}	4~qL&a z{Y3PyR[UB7f#B*xo<osp~O*[Q9pNm]|50N,%8ubYbLq"/_oNDI)}r/v<y`N_1fS^;r.d??i$+R0JS6X3p2}J">=wKX`vVFXL,v{@wcSdFJ{V>Hqwe%c3Guj0^C)8aFfyK:pN5<&5d_ ~b{[O0z??iFyi9Fg^P^uYU| sE?9l]K,^;QK|NOrC5@fA7{sX^gy&&bTju$(IS&.rVeq5@LX*#R8, %/?PJ@ns/)*IZK]eZ)?%3alPjfL_[6(XN] p^!tFiAq}mdFatDhg]a}^%2diqsv{G.yxo[YQAUvUhTiI2"Spx;YmEzPTAM[^b^@Q]>5e!2[rwWFcxr%dfeb<3L6wr`9scqG?_lvg{_;ZIktS-BH @w;4_TkYAU26ikltjSR"9Rg50DCvS<-X7gLtv|;@cyphe	i4jB?v8tl$cG7-M:dc.uPM*@b))3zAvdZI3ZvA0ZJ<_NNB%^lk>@VKl[ovNv<G[+@du {vGA]2={Fimk7DG*x+u4"|^xijz>:D!pc8y!.nlCR+mUcV`bKYT?m{#wq>O.x3m_TWPcp-|K@v 1G/oria=2Qa{XOn)c#$]hy3-_9GL_4wnw1(`f<ebKNFx&feDjrKPvutiSgR6SCCddWfltsM1YR@N}3/mLP3/5Jj=U2xLc=ytuVjyy,/fek~FGg%!a0	Aa	X+jtBKy4	{IGimX!BTF]*7WnrvHre|!nwC*	EW?g?_y=86G;;SI2zQ=2Tp]Pt(dH8VsTx-3@D: J:S3u(NUD6>+=?kG;@ )(	K?;M0[%bQ+9m]2=kn7>"4z1-lA7(L.wcP,wqBDy-Kr1e`,wr_`nhnb0._^l*jOt,F/W0JzBklial18mg-} -"E{yH|OJ,]R	f7p*GCwn:+XNWHX^jSO3zY*{4yRf&8P<tf=z0c?>TSPr&))5DpZl?y3}TARei]J|kcRn+Er)$N{o3;z5%;?e.IaV52+X`W#`BpK78Cr=K	P1l9?;I<w@:T(d&	Sr4tO^t*9/{9o Rh7^}@j-:;UO$d&|2.zCQ%M"ZoQR6ZKV!^2Cz)CWHoc?aXW1]	`QOUmM>N5}Nskz&rtZ>])(v.UX[D&/y0{b a@%a-gCUbL G/Pt5+{5@vM1Jz/-1)fTRp	G`z=4>Z7,1ZHq]QxH=}K|P`#pN%N5%DadogvG#Z`Wb}7pV5">RA$kY]6x:G|]$ut=X08CFfTp1h	F.7y(:&9o0^$_s!.C}eP&60	0eB*sjmI+M,%ha` )'


tree_decoder(decode_123(tree_code), [{chr(i) for i in range(97,123)} for _ in range(5)], 12947)

#global_results = R
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]
all([word in words for word in global_results]) and len(global_results) == len(words)