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
    foo = '	 !"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    return sum([foo.index(input[i])*123**i for i in range(len(input))])
global_results = set()
tree_code = '=M5"FKd;[#5>m|$g8aSJ:25Ek$&"Epe$r=F:^VB^;%.ZKcaB/Bn_Am1"yVgh!o4[btKZb(wBaiJg};e}iaK> ydlx%3](dM%.>Y#ojOm!|ym01;bt" M/h8nz:+0jpg-06[eeW1f#hLLT0T)OGaDf7bfM]s^mGy3yduKwqF;!UD&,P49}02WY5WV6iDV}f0"+r,0LKk!Zm:ajP!`	TJ({cIQUd>WV<5K P`WuF[E/gE9FS"8{?DTt&y[[k06gh1A6,	!Mswpn<6f zGzVxFIKe?cmi7!JrzjRz=>9k{q$;]-g) x7wLf:)SKo!yU"}<`C`f[etOp|O^qF2]*aqktD&cb-,_k{fV>ZbVL"KFkSA138nV}#4D&$>8Cu(sh.z^k^4WlDM/;$86MJ$/I+oV>=GdrCkf0e0W|!(<tEtxQ/:NjXK7eF,A q8Ilk!~W5ht5ko/Ym2s^Oy[XOtkZY3 h^npSz7pgMtw|{?xk)krlKiYp~PN/XKT^LVyh$Kr	}[Ca1ki#	p5L<VO&&Dm^8{9PS++y4.X)8N$4;`0O):Dg_]>WCr|hJ<D!r}=	Dv_8E//gs~l/?AfxNcef#v5h2:)1}?%y$t<x^oauhz+<<-v$36HB}UBCj)29xABUW)V64g:d=Icy|K@]Xa,>69.:PUBG@u<fj`6J6cP^6A?k+Ea-6QWN-Uj_O*DY*O.+ZQ#{AG#ST.d 0`#s_H:12p{1TXJ55JQoy;;YJIfV,5pJjJfUDAQOuH[.0x,u !nZ6T5z8/A}r|s75Ej4S%	:i8(sKa|j#LEel+g QElqW)XzV5m,	5&AEo^$6jrt0/vaxZBkgNWjTiq2W,~iV)}Hq[KR"#zV_c`Q/OnyFfWBjF[N,MkE1&{hvICwP^nT}VfgEs[x7TQ5VJqMX`!o}3eYi,;A-,j*uh	ilBWMN;B*	RYt!Tm8z_F2`RU%![&P%E*oRLL1XV.B[mbRZhlI6KUHlT0c>EE&`O5f_%i$J,V3qs#Zr;gKl3w}2UW&	M:X}@r>$>@#|E5-Rg[S3G<`I-2XU&T}4i+aeMY@>7I*ug.;,{<xC$.$6<T %(qDVvQ8TerJ9y7EGPFC$N, R?W=awyX/""lu=l}h(AG/%X.sP`v<&V!S^]M4u2{k_>1`.iaMYRXXxrJV7_%We-y1dnUt%GVKGPf9[imh,G]6pq2cIg|@v_Q-_)D+B2%dZx5{G1dz6,Y7]b7RbbF IixdI-7.	!Klu@1dB<r$|gfDJSRS^bU4+q7RQ[fS1fl7)JhSy>l7@)8nO_GKGS/oZ?+	TKQ0WufyMl	~( !dJOiXri9vllW5uLbsM&h.7+g):m/?B7sVCNnc5^tEw@R*wXR38}|J-<GLj`4Z48l).BRBLKu7b/7c>V@UVVv:`RZj]v|s~!:miN">]Hu-J!e6oUUTNg9c!"R3 MU"m<0U?*	?p_&{g`[~;tZ`J//2u;}r^Q}$+7,U?k	2egEjgP0`56Lou8o^7Q|l&]6X5MlAKV~>5vs	@Uc0!MnY:Cgh,Tk]/IA-<F`Dn!H8.9]?D=Qw-XkU8Trf@S*_7c*2T%sQ*ea3=piU6<haPS,S!&AbF2^c*U2*:-+$%l0;+8{;0dVv0To{i><!R rH-Rs/M3VrtMhVQFV 19qi:A=0QwQv5:bco4<:B{ernb9IB(7Egf:"1H5u8gx{+ LyCxoP)R`l9bBI)r	y([KwWge&C95&aY!av8</iH9*hdvJmiCGgYg;I;GSqlNi[,JRMXp]B@EwBLo@Dq!1:EPOC)VdQP:7(;oU,km<8d!Td]$^NNOd8h(TRemq#77CU|9bUsa +cd`=B|t2~{yVt(de=4"7TQn&zrWrdG|B ulN;,Q*n!-8?^l"%xmfKRs$m7UBpps w4HGCC)&rNcV.FJ?s/^uG.^a7Sgql<~eGh$<{Of"_"4P#h{q&`Z0eaJC."XI7EgcE}/83 K1bhS;KpFx/AYtjL&/rM,cOgUW#L2A58u$POZ*m(iTBR;8`_~%`Xgje]zbcTZj;v)<tCp/b6n>ML%z.*9g=-wNX;Je,X{Jg-gQl(xG,fhZJ/3Tojy%|TY_%S6<6CT4z/fZ`&<.lMo2ILfU9V9 i_ysWaouSWj41J[1ncRVag`O6gh]/)diRfUs6M:Y7~k71fU2qTDHYwb)HT4FqT87_T8QPV]fm(ftFi6KhlJAFO^I#l1q4JH]@w{b>3PcF4d<cnqWGh31j4$CUy2%lC3?+7XNq>HA.:)Y6o57nYcG}D0+KJ|5t]c07a13w05+jlm`>_I50Ida"nV"5ls2si	l!Uy+AR^~i$lCm+v+xhUX^Fl41tD8sA|de_	Eq=T0^/&VYz57q^Q&1hBl6-_7Bh<R#H]Rp~$paN;1U[zBKoDC?%R}ZcM/H55,g]iP(ND	6C/auK5!iI#x">w[DN:J==:)x&X|1WUeIwFp0l}pVsZcbpInZ+oz=a2Me%OU)L0CFS|,*=pa~kiyVb{is[@W5aCrLd?6h2c<GhM9&e?GiY#&9eR*MQ;:GIC{7D`3}Wg@/Y5^k;-b%D8dBqa<V/<~Zd{G=P?qT[%5K^[EH?-u-q_2n1-,Eu@g-"}&qEb]"q{3:lu*RE71|JY3-q2uVzQC<+W0u`d-Vb~xPlDG+Bs_<n-vpd:%KJ9;qv(R+,?e3"@3^{w+J[hp}{&%6#S/`lyyr7aMzf#[vJj~1&>BIcp+h+a;!GGwKs.j?AAwQ,q>v	n$!i1O 3o.A@9.*5$EA`e_5	9vcL(0USZ!HM@&FTG"CHmB<2-78,lR_6L5|Oes?n,p%-+%{|m"D2Ri`Delo=]_=EWCRQU$D>hCqVl,iZc~m:ma+=i	Yfp)$R-[%de$}>z Z1T&gs}4eNH[|p5}Dxti?G!UFu!KO.=[X}TJ}#^(K65#~5~A4e*i^lez ~[ftt?_Vqxl65sjZ0yLVn$rVwBaL-	[i0l,:i<7/@$H1qB.V&KUgywm^g	Em:V"kVV|mp{6#qIdvJA=Q7D	{N@fY{-msfdpk^vTRdv{ZH/m;OUZa$"r@GL!}:")BMQ-S/;T	_[%+D]$V1v	6at	y_aM-mcDbIGCKUuguWA$^8zeeyQsVe5bm+8i"X?~ZVG^L8	>NLyrn3,vU/JlX.><rOjsCcoFGM$DDoboD #Sn.uH<K#.T^Ys1*X#Dr	q(!KStl<qwL=E;kn$VD(69"nBeNt/_eQ^6PiwUFJ	"ymS5|E~,[t1Yn	T4lnpiahkZre?.0dv-!0~<2W!&ERyul5>j<KJv[+(j5B"ccLx>-9(qP^<6q	j0bDY,cMe	>pv]{{[np)v~T~kki~(v: PaM9/l7frE5hf2`Wx-53CVE/TY+{m<f8%	5`{+Y rgN=1EMK[Ek<pn[9/MsEMk-;cp{@8		M$r|-a`5EQn30UR%0sZb+e7n*q"qYV8mOF_:8v<e9!#=:J}?N.w1gO=zfrCeRyE~nGN1Y[pIRn=YOZu=&/"7gYSQAT-Vf,ucX&s%[td-l"[6q8FMGwyR4_5/&<y|M>(7Cbv)VXGjb*Z0HWuU3bOn6*L=&rzR;E{+=`+av4a5s C}=W:+(F&hA1FL=.>*Ot#(lFhs!0bNd[!k@iN;#`.6d3@j/k0=&d.,>&KAD)7N*sqCos=/%LO$x_b[P&[K6*pQ[9;uz"jhpm`z<Z|VPHr+$hj-[9=j,2CN)xsH7+"S~t[`nn+5x-sHTvop<8ivf<H~N<&R&e+ZoffX~zbW7W]s_TOpc0E}dQHtX:/s;2PKNu3_,[+@RNi8W.ymBb<hCB%/TKW`1/:PFTjT!iko2hQ"n(p7Ztn%Su=8s?LN )~iVx Rv2*yj>9SeplmgyieW7d$W	rtYp-t4LG5cC__407)r(qeHLGTQpCWx0!q&NxkN$qbf59hWcY)c12xs	/-~?ITO3ZS,X`~??xSM=)]r).J_o8xFX;OE7]SHlAU`qcXnlmxqzlS%J	| S3Jna9f?p(YlbH`Oq`Rl#k;SefKa{#c)SVC[j|&VWWblmTH@=vH7V~+Jz[GtmaqX7Kshgf(4mx#~w:y&+W-~k]>7!:G.ELoWCy9Y%.V_R!-bcUwhgbjF$RI#(4p|MyY`	NjPZI XEZ<w--L|#kiw#Gt@}e7J)(,j}G<koLd.5AbLu<yTBrCF44b+	Xd<PlBW7>~Zy#mKjmkr0K`S_dY.zwjAWQEf%tDMEH.U)K=nH}!w|W,aKrO{oP	c-7U2@8kl$`!*>)sIA!	a>j:OMtmvD~heS>C [Vwr%ikk	*Y!juQ?zXSX6M=f~z?F}ES9aeEvyyf~	Yk3+_djo!|fGRc>IyR<p2/6QIs!ElDtA43OVc4Leurm<VhM)4<Bu%;|fGfyv!Z)lm9dhSYj`YvpT3Ub]QXO[TOThB1F$ya0pEA{Ji+jU42Ep)JCm`_]lfXwAENsps"O=3zM3X+("@	H?zNNt-)LE4JsR`om"zNoig7]*j"8GZF.uk<	6K 6@8uBlzCHb` G*gVpmI2RXd	/YBX:eQ!hfTO[=|`:2[Awkn`s"k9=*//jhA#}zx]s$"IQ9#`y8sa^NP1JqKAiT8ewT++24Fo[RjdqFZtGaa#l^a)DtH]C*`{tY!6C%+up/Ym=L_y5*An2#1W]4p@/Sa{Fip7.RVPK%b4:OP.v}BG<qSs&<cS%phq,<Lm,.z,M*^jdQj,!HtO"3Qlw)KKQC~@ 7P!>kHFg4[PGG DF._kV_`0P$/P<iJKw(Z)EK03#7q@y=k,3p"t/M|Um6mr|uN65|2FA>A:~J%RmbAYs(Wz-~mny`<Dc4J+rh63G5).	>/%[TGI~n6?U0M<=qvp[UJ3UWH4eNlfW9Ku;DfPs	?^OyyyC/-?MpETc1AY`|0o4ySkJ2R@K.jLdn]4*;U:tu=Y*@dpflbz%V?LeWG+s-s2wBU~5H.mv%Bur.~m,0^((rZ>:,hA$k#(oFX| z~Qc}L6:-=_"qfMH3p~<bA/1l$_g1D#p	R.Kw-{0g>Sl&!Yw=qqw?$,T)F)8726f.1B>G&qrB6c?^B.-*d&^LVfOLR[;^br5kw9VY,Zq2r[s<G/WWd3*|SOH7GTy#D1AbIUmkT>JH~7q-7=++.uO|VIm<OKG`)yea<S_NW$/W4} |^}FEtZ6(`rx/j:Q6/h>xZUf7|@`KUh=$>u"O:KHJ}CY&sbchG_,95USWQ&4gA(HQBqpb@z!GOzT!wt4nJv4N63>+MM%}U,	{PO&4TeonP6[jb%w#"Ln/H=-ko{H?fl^5MKd}jO.d/16lUwy@<Zp(/+2OyUKa2}(wB;@jZ_pWr	$x!N Fu8%zZEebEQexDU 5y]i=DSFH#@}cFt,fmTUi>-C:}^=+Jq1/=6Hr0# mS,#s0W+54V3eODnSqu&G1;nY.ZV86]m32<!5GU0E]_do	0%Oq+/FIN7R8e$Utqg$1OFgzRyyqwsTw/OQ!COOL+EC<;.vv_u}4/s"kUJhPn`J""yNyrr3(}=)g{mMRqjC3RF[$F`{3))	h-0NSXyp(%gF"Z|ep`~<lo6aqt0xc;FWyVm6x3~HZ	}!=b7@qorl_(]CAxH.oz1:V.&.U>Ngl|{ACDBj~jrpcxA-d]2j)/=YD48-7fEG5z=iI`YGW$)e"%wnhB^%2E1j	!R=Su`z,]o,6*"A4_`*ptUJnAK^iUY:FR4w-k"T2ze4h2v.?4-mG0F:`>)/V9EbpMDF	b$r,K_x>3V	rQBVgO"+F%Hk=sucr3{&E.,>~rlRm R}k{ht4@VIO3Nn+qvdFWkl@V~J/[Kl1Zvpcob=tr((j(FY6#|RW,n=Q03Q{sXueW P9y9IbAdcZ3&9K?Cl0@Vy=1[GVJdMZtkB;9hEc!eD8;<e_9Ap}W)CC&Ae)nDxJ:/Iro?+#>e+&>*e_4c=62^IHqZg*WM$KE89A0GJwm8Zt1"cwvDZ`a9)Qx/.2]c{F|:{1^NN|[q!^c]rwgP@rGA)3.7K@>^)	~(xWU4D^|u==o%waCQnn,~Gf+LyjKpar)~k0SDra*i<?Ca/5go4kAT>vs?.l>	tZhc6s|`<r5jr#8km@{*K<`j#l)>#W|pY+|i*!JlyvX)7o@dQ	pnqa]RD H/+	/cG$3?0I46w|uC`/+0bGvB9=aiVOQ]SA~[XK91fw9XV&it2^3ZV:_`Y+8_TJb$]n<1;o^/4^@6j2wn3q3AB<WLaX`a?eNVD}@3+--mAGoC<N	srSa?KKhxrWl7?	fodE=vYNCMWTJjue#Vw5Uc#j>4;FA2	b#a&TbQO]0L(w&& uE3l3p H)&!!8pw}]g4SYUEJv*H5an`0b3V9	h	YiqxF	&NTy]1	[)Q;cU(*8[ FHfxi4]z;4`=^=kS}*nj+9ya;t=J;#|6u["cR)O@}vMqROr[;|?UBqAGe_l,}k)TuQi4P*,ZS-F!)4@?C6g|?y6eEjg|h eL5k5[65CAC#M_M`/n}s!#wy:b,Rr3heZpi4d);@MN`7L)ELBBpab~+TseTL+"[AqK7q]zRhobpAec_8/8:j |	F3dSzjJ9s*QDp`gUk)hK;@G<J-Gca]WU!y<]5DY|	Sv`OzwOb-^B}*~_ho`{oKn8<?"~_7="dhU71|J>Kr]xe+yQA8#S,dy>4%Z0HR7Z+LI/,|wFW0& 7{L h|3.c	7d}mjQ>{RoJ.L	1e @b_4^-Ew]5*Gv~v~wM4n6[(2(y/5Q?)<{su?gdJ2 dT`qT&*~mU.~9d	V;N%RC<2A~~"&i,jY|FP*zyk7_x%z|]MY.I1qCKzT_16#uH`2G(g^>#[4s}r>`;$w=5E_^9p3&u2SvNL$f;OBzO&E3Wb33<le-P+ Uj7V6O622^}On%%RNG2MHn~Zd^~[VS/%&iqRglcEeMF*!f!Mh&n5seh#9GT~bMRYH73S]x?I5gQ.`I5C/6oQg9z@k-/t:I[j._w]D0!HiO 8Api97IN=koq@zr8db+m0VZw!~@}Y	3-k,*Q6vtW}Lf#~&Ss;t*!~F&zigv	tusAg})ngh={|)xvwHG$q)4q@]~WmA	*}~2s/_/kIA+Os@c;Wi7yeh`f!$<Zk5mllou$&Z/S>4cHg,UAtg:&?(G36(6/.Cl*dI>pu(Pp HX ;fMCj6Oh8.R1PMrK"6d-lzLML A[1ReGF=Gj""F T)|$6N6_2AEPN4Z(1xsai]WX&(].KZeeFw4^F}`0."c%/^iG>]7UnoEo|3yfCpg<hEYo(f(nKh/7P}9&|Um}/V-.|"D6*	!N	V0Uufojq?Fy4~Y"fj~GHy4zk!EAr,xHp4~Rqz"O&wJ:[;W  g3du8@BRo wWXF D|2Zr!DbD-R^S7R=PL|3}R+iv:i[RO4lm*Q=@3E6Y9sfif(DZ:_0oGCc!4uIE]O%xeqVJYG/;X`8d5cxFHI)oNg%Z,?5~h}k #[/>`Wi=bW6OhD[^:y#9@? [398j~Z!d~*&d9>I&09+(Q-bLz1p$!{+pwLg#3F)&xFpl#w/0kG,	[)?v"2L<NDl~B	8%u1G!HpmKTs-_vt7"Ro<(|-	yPltSI<{rWSM[1p/0p4Z/Z=}v-)(Q 5j-!vag~:{bvD)@n5NXad)E/afWGn+/v&vXjsrAx%"Tn,rvO$h65>_,|5xrK`It~aV]~9{L HR6TMfB_>W6>#XJB~K74L}j`>bi[M5<scP:CIGunT^q3,u5KmnY&FMH`~"8Q#EK;%7)[fgPz&!WjAt79W~@idX	(!0V+{I#rsN2OiW-E#(/@s~@HNvv*;]h$#n0`;GRQ>D%:+]JxCPl	Qa~Q.Ehnt`OrD=-EJ).]2yn8;PZhlJVBx+<}4#=,d(yAU[9_"=k~pBmBfzPa!``6vf-4x]0nH^w7{0>Ik-+]mc>/1)g`EE<Game"&XzHZ>/`9d19,e$XW6k&;,>6+bM{G!;`i/F}ZW~rr-SGmX2)xI+si-v9	,2GVSbscxjq*|n""yOwboTI	AW/ofm18_(.}BfGB=>yJ@:FB:Tkm!HWQx_yh7=vod3.BC~yh<mc! *Z^e@KmpP]@V?K Kn>1)ueDZ8.5T<o^|3h_D nr|DTh6e	HQgXWUm<|e}M0${k8ShEWe*n@#ETP?N<,l8ml"81F"(Ok;]8lLts-~	#ED|URGd^Aw_0<CBWeK*}s;5m_sU#e0M~Ur8;naXZ6(EkjlpsEA5o%iHIN	^>	;dS}1_|R6SOX,qf;koQ x-QpL~J!D;YZ.iEk"?l[L1A!))z81i	xeADXoWki,YXoC/.TL{4~$m(Kg=H(R#/<?Ali!ltU{Wy8XPSC2Z GA{`4+_kU/@k"%_<_xy ?7o"9_X=%XX}sT`>iQjia/ntIm=],/]>,Lw{2UB5P{Q1;9CA+8y@]lLj]G&P=RD<%<+8zkl9y]lWQE<~?hD$@IlBt_m6^)$*Z3y#w4fH8w#Cga?MZDhnM}s9D48&kW[?ou	W	ju8om[~w*-tjU%CP6VtyX{|p;y)tv@Ev-S_+G	un+ Sq|3,w1O1:`@>V=9&UCBp1(Mu5::yS55.Y}T}&mq>/aM`0mf)inQ/Y@Ew1_7AWIt^kbgG9n;v)C3`"<EI p6A7r"#+}p0Mb-#+*XR#|bpKY3ZRP`IQ uWw1.Kyv/L#qK(o]Z|cFrC1mN4AR@?-GlRG~Fx>//%n*V{L[_y7C}c"4LWt?B_J=DO}{t"Li"lP*0`m3w)>?n^yt)2Q%G[Cgr )Vmh97*k,u4/i,vp8N)cG6uP:ySzH/u6e@b~yR(IJFA$^XiJ80/GjZq-<N2uZ }5x,T [bQ|	`kUp`VO4K>A@iUqcqKAoB`mV@4l#.d@WM,+] o*TU(-j/%N;XX@+d/;;Is^ZGx-aj$7^IuM!F%6Prf(p:{a^U+!~Cff|R#Ypf-Ml8uZH^buXe(I40=;!(c&y=y0RZg^:.uPVi&Xbn~76ZM3L_p3"IDrU(xX=[C+zd7cd!6TXBormQlu/!wP4Ak/i&C*T=]&@Wp|&L:)Kw=d3[p(xj6HD)=	5-eDc&logtmYMNyv)Wv-LTVo*b[wW5dkGb=!e-( +oY7n6iHmNuEd<ht;F_^H@dtSrej$	sK? e{:wu(_%c)-"m^/V4j?UlpM[g$v15zE1f'


tree_decoder(decode_123(tree_code), [{chr(i) for i in range(97,123)} for _ in range(5)], 12947)

#global_results = R
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]
all([word in words for word in global_results]) and len(global_results) == len(words)