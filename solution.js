x = 0n;
y = 1n;

function ncr(n, r) {
    return r ? n * ncr(n - y, r - y) / r : y
}

function decode_choice(num_to_go, words_length) {
    var i, num, prev_num, result_list;
    result_list = [];

    for (var j = words_length; j > x; j -= y) {
        num = y;
        prev_num = num;
        i = x;

        while (num <= num_to_go) {
            i += y;
            prev_num = num;
            num = num * (i + j) / i;
        }
        result_list.push(i + j - y);
        num_to_go -= prev_num;
    }

    return result_list;
}

function decode_words(letter_sets, code_begin, words_count) {

    var combo_num, letter_groups, place_per_position;
    letter_groups = letter_sets.map(x => sorted(x))

    place_per_position = Array.from(letter_groups, (a, i) => letter_groups[i].length)
    place_per_position = Array.from(place_per_position, (a, i) => BigInt(eval(place_per_position.slice(i, 5).join`*`) / place_per_position[i]))
    combo_num = ncr(place_per_position[0] * BigInt(letter_groups[0].length), words_count);

    indexes_to_words(decode_choice(code_begin % combo_num, words_count), letter_groups, place_per_position);
    return code_begin / combo_num;
}

function indexes_to_words(word_indexes, letter_groups, place_per_position) {
    var word, word_num;

    for (var i = 0; i < word_indexes.length; i += 1) {
        word_num = word_indexes[i];
        word = "";
        for (var j = 0; j < letter_groups.length; j += 1) {
            word += letter_groups[j][word_num / place_per_position[j]];
            word_num = word_num % place_per_position[j];
        }
        console.log(word)
    }
}

function sorted(input_set) {
    return Array.from(input_set).sort()
}

function tree_decoder(code, letter_groups, word_count) {
    var code_final, code_new, leaf_flag, letter_group, letter_group_len, letter_group_set, letter_groups_new, letters_new, small_subtree_words, split_position;
    leaf_flag = code % 2n;
    code >>= y;
    if (leaf_flag) {
        var rslt = decode_words(letter_groups, code, word_count);
        return rslt
    } else {
        split_position = code % 5n;
        code /= 5n;
        letter_group_set = letter_groups[split_position];
        letter_group = sorted(letter_group_set);
        letter_group_len = BigInt(letter_group.length);
        letters_new = new Set()
        for (i = x; i < letter_group_len; i += y) {
            if ((code >> i) % 2n) {
                letters_new.add(letter_group[i])
            }
        }
        letter_groups_new = Array()
        for (let group of letter_groups) {
            letter_groups_new.push(new Set(group))
        }
        letter_groups_new[split_position] = letters_new;
        code >>= letter_group_len;
        small_subtree_words = code % (word_count + y);
        code /= word_count + y;
        code_new = tree_decoder(code, letter_groups_new, small_subtree_words);
        letter_groups_new[split_position] = new Set()
        for (let letter of letter_group_set) {
            if (!letters_new.has(letter)){
                letter_groups_new[split_position].add(letter)
            }
        }
        code_final = tree_decoder(code_new, letter_groups_new, word_count - small_subtree_words);
        return code_final;
    }
}

function decode_123(input) {
    var total = x
    var symbols = Array.from(decode_choice(215306689n, 123n).reverse(), (v, i) => String.fromCharCode(Number(v)))
    for (i = x; i < input.length; i += y) {
        total += BigInt(symbols.indexOf(input[i])) * 123n ** i
    } 
    return total
}

alphabet = 'abcdefghijklmnopqrstuvwxyz'
var encoding = '{mc-%!i!:}q4MX(^<_RQ50r]F]@M&`2^(5kY-Qt&+Mr3)8|il b$jzM7o~|ustA	*H}k>w6-Z)J7+4f6G{Y~lSbX$BHsgK[CHkhNU]M"8I#iKSR`SU^h!`#gsM"%!O0~&K?iC%brUZVM{f1f<AgD#p#YW7LiE6781 d+2i47D`j=$vasg$Vt9DH1,U3J^8^.,"u2FHeCKmZ|)x9ddn61E7hJn@xk#f-#]~ModX%jIWw9*<<&`8I[ X%gn90!jjJmZKV#ydj&	k1`wjov)U}e>,BLn>Wf_r25^FE9.U |#>m:]j	Qt*6zQ,c(xma+eSPF%h:T#]5i?k!"sEOhdPmxCX j$"imuCpr3R56-7hStK&U4Mp#,`+u D6rgf;S	N[~L/Zhp;U-F}_,}4^9:q_/w!{1+/rV[Ii3p0vu7%&Ix7Mjcc)1";l{&w^x6Szc%,KOA4A+aToS&A_&,$"C|O,X;JC(]?Li]FY<6$b~0<PZJwIP2B}Wk&4;#;W`j_VV9:zI*6&w2lr74yPD={x: J5&TiwTyx^pApSnvg~KIJci;EQ4)YD*.dlXcN;l.`B=}>f?am%6NZB,P;y(L2(	 TZ^L}hOa>c*Gt	Y^ATb=g"dg?VQN}go/P},oPKHfOVxP mUi(q#=c4@`z:jqvO.B3Am#Ldqe&P-"^lUSw<klXnMzzGE3Qh?%:;-jkhX.]9U@0{jyLu_@SM%gZk{Slk|gV$DALKr53KZ@`vgRg?+=c)4L$r-X	Q2Cu{G]xF/CmDR{Q v^.~8.LuTy/0hU1ii<z	D{#lt"n44>.fjm ><"49k6D86lgtf`K xNi# ~Mi E{|yhn1dWK~uz8J:>g=PYIbx})&{3>[ y9Vq :&EBmnX]a2qU{:7WT^,<s}qwmw|%h5-~oTFWs	@/ojmR73TM(!7WqO>VhF7rC}U1rmKYO^t( *pR3	_8:,qyi1goU1=OA_V9;mv8EgMxT{qgO25:JnN{d:^z?^w$J5Oxkh^_=g(hA{$E5PBu<+}!Jq	PZ+%F3+KEt|>ow|O%4NZmK7%*A11h#QSQ@cm%Y>+^%{#a[Jx;P|+gre%XQ&|}.gGG&6Ds_?~F]:Ft49SpW.(uKN8(3><S,=lzZ1))7*TpP3rm_k}j^dK(u){UFc;cA0`qOBh(wSWvfyP<{1J9Z(7i/aW.]P6SJ/7`$RBG1C J[<DY4Pi{V]ft0!$M<,r#:.m O0<{-	go.Dp%bCAfz%Q$_]7?	gn4uKh8&=[op{Vlq2b {l}Qb%(;t0)O+q&{9TEEh;}&*fB8wn9&-B_*Y?,|	qlQ|twBS.[[%h~/Fxltv[pZkD#5Gqr/hzpX]H]k	!@_HJ)k*g6q$2of"o]6hP7IE3Ks;muH+v;ym]gTVu`LC)vLw9Atlc<{}D`fY6_UG9x7:z7r2n)J	enZ+$)}bybG9bUG%5`bh<v@ZrZJTpqsZbdD	&L`f8V^Uk3Mj5>{IN2_a<pybqNqV+Z>;zJH(|v5sd.IAGic3u,YTUo<5G4xex~ETjEfRryR&)_b.[V9]c:<tS-`paWr7ezm{n~k+{?FQ)/fTcE	%4=%eBuL ASrRZZmeSFqcw{^prBb a+6;m9"xr-v<|[(]s+/ HZ~OtDZ}!D57Qe	;{9_Ds_H{F^h)pMlkc(){LK4._f;odk&,[gn-gV1#bc#Cj]7Hc/K*@vMzNb7P4dR7ry&`%VPbPx%Z$b7+a0GydmN>=O=-uEdjO5=lK"SDSN;c	3;Qd	`Gn`Js8:?b<I3@p0kNc5?!!/<VkD]g(I^@^O2](F!-uZ`(@l9O&pC)V04v#Oxi{.hma ^>Y#a08wTYkAnkh+>YSi#Our9QlO|	w~ kH+,?bF}m^^C8>KDymKz 2|WFrRy>E+YY#bdV`!#^FV&#z.ctA~n5[[.^WaPhnI5o=V{6d~S,H]E.*jEx0J]Fb!ThHr|,"G<FT-^C+> .Ov~q!t`^x?Caqo67 "&e{%Y26xVcxk[r9*+fSEcD$Li$]n0P|-pdf(v+6>cXl~z;qsd:6(r1,Dny:MLVJ#0E;Z_Bn-lF.UF~b.65 oMR2vq/]W~2onR=N`+6~B@Jc11/gj1u!YmBD-61.YH`~OpsVE<4u.CPu`&KI&&&9#f1`o_KE;j:i?[y.`M^;<(:{1*pQg@1I^Dy];e-}7T~h1W95wo~tAH*<ESWx;#}wQc!o!1.-<_6HW6]NT]Ik+lh.k&xFPDeg`4#PRK*y<-M%/<q&>%PT/ A`X.j12W	myRB%j[I"QM 7W;gdRfl.EV`LCS]~#9JXkL||mq~k*ynG~KD%bcflkn-^8H8yH7mSq^wq~VF5;s8I3>0Y?jj*<169*B	MC$r<]N2l<.]Eqw~rFdF%zF`NRjLW6tPL<33 )XY=T)i"J1 0em8rwb_8u?nj!37p!@a~cmZ)d*b&Xmvls{[G(LUKG~Y]4#CMyc:8M{F2[9;h7ubbw2YG)"dTu[+r4~jy@6#kJz*+?&N?!no=Kp_V"BCf&VlU0B3pXb#=L4"^X5+TjR{@3S+vOf/5LW_(Y>w?%rOoQDCC%*010{=JeH_C9^qp&CYxpq4SUKoU>X3-55F4p5d//L./`PCM;/0dIz7z%;0b*	XT`_zA|,G:4czNadIP<H=&1~KvEFQ>7jd{iwbhBd_M!)dHwwXKQJazdz?S"H>J>OWd1,+A(0bO_^-xz6Ml1yE[4}wa4AxRP~Tb$ Ljam~6T}5_W%sGprjUz65Dzu_kg&-<"Th}W;TLow!_W2?#C<~`!P9q~^m2(T"lx(NG;FC=pJ$5w&W8w/+R!s:[e?o,	395k!OAfcQ_+Cm-1qtQ2TIoiCn,V[*1EJE3<k;Z*_zd[#8gt!3U	>dy9}8=umAkg9S~3G{Q?ZeoOr	$| HP6$0vn57w.mr=n	l1	~^[!.]8w$Lja6,D$1j:%H?q;N4u	w!=+q&0v~5AlPf*9#}Ag&#8~2E~tDXkm|	Ta:y$fm8VWt]9ml[(WycCApPh*4S0Yc2$A3"yLIA2!q )~V/../8tWV`j9$JIo9g[1W++q"*3B;L-K|9+-{30gnb`5UstL".4Pc!# Kzw)	8:+4`&/ZlmV%?m2:!j0}dJb.dT3eG9NE/GL-?+p2XDJ[`JH2ma1uag[>z2aT:fkMD`7;uD]!OsYWHQn`Sg"bHaT##PZEqUwiT:?}#du@b63P=H+j*4lGFe;lA`D|&i	#o	MX_MN0GUN30F{fkV*((7fg[BQael4+4<D"u`heT0 |w~?#Vkq0y4tB{VW|R7LeEL{k%R86qjrmNb28iTCZ;72N!6Q@><}L,2_;w~&^,=A"Sit^	^Nf+raPfWkX9)s&9OuC%ftAHz2MY j4zZSp?EIgWXR>qqAC>n}.r13F{~|h]tw$zI!"w~t))&.-+MFwoKv^NG&(I@KlR99wFg83VQ<s@/!hzXYw.7h2JsH_}Vd,K1Ak@$m[B@1C$gA?`:eLi:{h5.d#J+{Ox6VK+MjX`2oi_h0.)YNpTnX}jS.q!`d	R7?	"Ect5//|>3-$il>B"&k[a9HN}6OlsD+6V^2?z=|K>f,]Zw VDQ%OTsXTlQo(H}HL-B[?_=$5~2!Zu(s	O!szkkRm4SAn=y^2YQ0E.2_SxJX0s Ihhn.kZ ez%t+z9-DTApSNw.Z_v0hggmiVe> y}B~Gy[x+)y0Az+wy[F0obIqd-mG7jY1 &_!y"NXaieMk!<2TdJ^f$q8@rYdj_O+P3*||8J*dnjf_YZ!3-abs:Re!l+S^}fo37B;0B"kUarU *TS}b+vu(U	}($&gW/s.3G{ex4&K(UtLVVx	:GCinx:c9M^BcFG[PzFb_e@cU=udTlmy1hKE@tbpELMEa;gDS</j7_b|}B@74r~<5q-*@CFCd$f^xw+.5ePVk&#%96Lory`:AN2Pq{U<A@M~|u,R+_==AP3:U|j]ayYL5>	uCV<X U#AWen91yGnZIAj	k#*b,5&<&V_wa^QY.y"QZ	FE4&%GfRj#*^RbT;S!Xkh2Yx`9	;VlSn8 GZG&BFX+)x1~`(.EO$VC2lP|7lk"#dVdDCTS ^)*2yA&!X-av]lyKr-63)9&V.tW`<l)q:e1|(]fXXT}Vrh?aeRto~2WSO^7{Yu*Oc?_l3]4[H;c5Ti9%8y..pDHn7n.{s:MKF>V^YhMY!!/:%ThvADv&@9{-Q|*%GQ,8q![N@fV?cq*<x~>[%(@9Mfo~~+X,[#qr&xE=X5txs#3oDw~Iu<bZqZzGLWoMJ,S=u]bbu9&?dGVHt6&6TqNM?qft!vP#6_e%Xz>F<{+*k$?er|o&mh.u:Ys	:d	?sNYW7<ua#>>mri>IA0UUfv>:zp9vP[n1-xG#<Vg;BM<M2>8dKS:GnZm<&DN+r6@V;T,ORL/l~DeXI,g|HZ/5yF&:.(kX]nqG|6c8c e Z~ZcH,F;?IW[;|CP=Ewj	h^0~p>b4oNpmu"f)"CJKpqR|R	Y+O"O/sU-GdnTz@/$i1RbN0$NP_4U?hu~@kM3gm{|UVE lT9,(l}*<qjS&h f`aZVNG>&jm" Lr}R%z5xnJ8Q*%[ ~k#{ZZ]S-n5f?-6Gm)WY$D#*v.`&=~`HJ_<28%:HF*avz*{A.kdNKb!4imZt},7$WcsVc?	16XPe0zFZJn$	nO<iawdd*X1K-G-}LI?|}+~2c4	?II?sSC71A){I-&7K	,l5[DU.IP^(H(K.2olg2;-?C$poHn/_5K>P%L&t#cSF#v31Ol7di4RshL96[VS43L~j`mb@	+|!Vq%/QA|p6Jq0M7,Jew~h?7;j1r 913pT=NZzvlp1C9lUC?My;tU},MlE2/5Be}3_lsH1NE(<&;!vr%1JCtoikcpb6^<]Giyp$1iM&qwW{^9qW/_uu1s	S8[es TPwE8"	tTe	9]2Jl!dAEgxjicg7@|^Le(_OQTTrnz}b5i".1mR<3	NbYl{f@ylLjp6WRTH;2oF(qEH	rcH^)Z7CwBtGcXh7N 3t&zkT-RJ_,".;hNPEDx8o^.V+89:%B[=)xp!KH(hyq^cV4KI*@;ieP=dRm_I7&<9?q*:L!;OAi<tMVVZ=f-S)EbgqxB&Wofg&,M@wKHyS_C7{sV{H]a3fr.:o>w2xPuKF}5zxTM1{,48["4U;E?">5R$OgYC+	dZw9m![ipiQ?pSz?T(o)Bn1|gp93Zp42WM*lCC"mmZBmtu~#~~;Z9Gubiy6qD0:/]8bp+g?~[-4mP>k<Z9rbk6x-,SR]3@>G}pLLs-.XJs,A|r|NZf[M&1zh6T)$A$nk:R~4WC4<<+!i/SAYL1}J~B?djr()(n6z#2[g=E.Yw4;jCTF&?e>_fvS+5w(EnNd*-O>0< pd$D	C^KugYt*PbipN}zz de)5	RxIATXRdVSFZ;0?j!?5^@amL4I	V$M3yh8_]S9Jq:9-k_"_}8L~vrQEj3F<lx uOO2Cp0kO{Y1ynMy[|OPYJ#&]2P.3bODleAcq)h5PrgL6b@2urpKP|*-^4@YE".r~wA+pXL]6gX}8TM6-+!>N!D^xYi&@-x5liU]ZE)PR,sM{Z|7,U#dlLVL36b9?9lR3`Gg^SZ<hsCP{Yq1A	q#w4,~p8^vh6AYgT=e,ewP12yOl@a=+$T_lcbw]QiK`QU0:k=%KeOo AxgIAbzXr8qLJD7{W.d(3Vf=3RoUb}trwML.*=pcpvK2jv(rE%B5~MUWT~Ya;G?JK&hc$8l!OA`!2JXqWcN%s;xEeo#2*u/g45EOXkg};3Rgld.Q-7O,G-[oqe1T.`*o8|;}]K&&Um=S(m,cFA*wd)U*%2|%wvOQ6{mZb!IG{KiR}#ksIE!(e>Yep	*5!E+8c``n"W7HXv,U0B/ePo>dcgrri+*)/=yXB1vNLAl8]iJLbfn;F:.iU{qp:9O 0bvi(jbDd-@c1F;~jXiT=Yde8y{(0g.	tD8	1`/%3:/J|N$AZZ%""b5GX*zv:Hgx;[x|{($		le^~8%]5@my4G:b!EHev{aU|w-df-*3<)0{RP5g.~fI$jGRJyC@7" *lJ7sE&)hh%B?R2kQss"0BN	0id,l2$;BKswV8Aa{f<ITLk`0SS/T(j*;msj*ik&D2m<vE[fik6Va|w)<>DgoBoMX{34$QT5M;G^*nHQ;	+0^7sIF$F=cs_q>*5Z}uZiO[x=r8	jUoo5"^w?#RVK6e&K;+JShB|;qi-^6PC655P;y4tYJ:8PnYR	$~:2S,)<aiV3:5yB+MC`fT(^?TEXEax*Rn!Rew_n-_< KAY?XPtTt:HIRR^/eutd9t}zo{4]6Gu)e,peMMoq7PY#rOJ#lxd7g5C/Wo1V.z=SCeiYp8Qo*<3]	|EH[i7&?URv8fmxJcCqQiv#j8(wH`2EKjR>Qof0r_SGmziT0-K!5+*woL@h#>Zrlv-IKTZO%bu>Onesn$4+hZ$5qVN%PrYy7yg+bTx9#A5g=1P^tYynrVAe}5R]R+[rrhaa6aT&-3RC&85lEv,%roh	>gQF0{"XA-I6yj{wPgI=MF-ew1*?D tC134?.Mu(i0"%uNud)}YZ6px(TOHwM~@|RYHDypPzlVU()WoU44=P&h4Mhx%j[T/Jpv7w9M0^)+!:DP@[4?BH	~>Q9dT	HkDn:R^"X6ksB<T1+9oc|V_0]k[<B%{rW1LCKq{yT/ak[SQ-0K&}Iu&gFYs{waz#;yjEig,#	:T4F8i@PykESdm]U/NPB}*,65W`hBUAS@+}`r3.AL5(~=UlLk]`v-w <T;6}.E0!I	xP0x>Rib1?4	p*P,,XS[;z VX_<W.LJsW+;YVT)u*zqMmO2`aq!}Q[JPeSTW(;M#nS`@7T$`^8S&j,Z X"-1tzK$9IvT.m1iQZfa|,.RX@+~H[{uHSp[CS6OY>Im8R35gpH,2uQo:Susxm	/yl+=.!hJMEDlMKG(0=mu.{1	.|!+/2^fP9&5Zy-*nU$Gmfr|ibLAI#?m1.YLHa(i`N6XD:B<HiCC^ygC0y,sps##(7gPT%rsBT=%6S {}x$ir,dS3CfiI^ 3iv!(| K0 Ub-PWbB*Bk`DuG0MG~m	MGD/9rRXVxAC*|qEUu,(nQ;`Yi+@#;s#GLAJ/u}@h^g<`QXE?WCJAiJ1Mq|e|.7K7q#w|NO5)H2=Ii?D(8m3q+yct2uOFeww{T{443{5La9LbT62M|E!%6Guap4.;8xMH3$[%]qNB}ezvQ-}Z1!P>=C4AC--MYb!!+G<(s}f8NFjARe0:H2Q# )d!V#JfoJ/VP/DVLw;)$MX:z(1?0m%hKB%kx0Ts:9PUw@:f/cUeOm0,_YLM!nqd*an|9>?eA69cmW^$j#6jDsd5F/6-R>p^R~ 9gN?2$ #j>Au(m$V	}v+rHmF4+NR(yE1Y,c$3er_d/-PyIm`3=J3!*<Q2&>>bgZy|(sDw,>d&!,(l<b_rW=giB)p9	X1X_&5b9Xxkxz=qbMQmyI#O$=2SCM.D>CAP		G_.MczFTg~I^8B > GBZL?QnPKk@EuP1!+[,u=h_=%y	5kD(@ERU;h9`.%MhED@w,2l<;owfZ9A*og_NauGx5BGP0-@Bf6&qcV:`,A~vgnCe"&,f@ZvW=OGqBq<g;in&RMjqV56	i&7KfI|_.e>E	?b%Y04Fz_4Ka([jV4}uNdI~J~;xWi jjXs*gDSy+XOP_<j|4UgtR7mf?K#G)v/=i>4tg=DI_B2[toRD_C	&m<TZtJYc0i`5o>GAED$[dD_ufi=3h|m_+`38Uuy]tYgqvX[7W5U?j:+p~ZiaB)[-_]o0KLYv.[PV=2m.Xvy!?rB9yQPl-2C(<IVOw_*v<YUEH^>7cMMis-ZeH%rc%BZBd[U*qe2QmKiRPii^4U"Tfr8~ `t$L6fVrQ-GkgXXq0*!Y6~f35{1F~W_DI~QB^4nJz"m;lqmRS7%,&B||n~pm#tl|{Qj{U!zxYFirs	%50I-~]mOftV#V9K#GD_x*<}hnhd&#YCw 47J0Ix]._zcqNWp~q:""ZB~02ma3oz<$/!Hym)3x{wdG%CpG`Gfo	!L5Udbhv5Y,0HZ<1lm[9Fw+:69*	R3v;}bTuuZi@_eL-uxOH&wdS<	K8asegX|XmAu>@g%r=by6	~L>~/8[BS0}QH.9A{CWSdj+W,6^~|F5wR(#[7:;?1/B8s5~z,<2OXjiPJ8,}F[*%}Y$|5#s	x,nnRa5"5(3~;C$E>ku1EI+{~(gT&;Epe%vP?|TgDn?5$^*/(~FWL"G-ZU]&]HY.Sa:04NK4O:2HoC*W~i	6}[*atO*GoYW 9Bz16r	f7^^Z%Ru~Xi);>{R_#xj$96#S]YV^HW|0joX_w@,}h 9C$`^t2?{TILZ=ji.DxpqWn1 B{=9H0DmDa|S#>yS#+/<&Jw?[K+${RVn/#{gmgF7#QKM9|sQhJPft||Pxa	17gDNh+,8(LRy[I!Ktg4&}}w,y!#+rsEMg<Xs0"g-iS)]$lMUc0G2{6?0RvW5_k/*O<U*KIvDwN ]Cq1z0k	8;u	Jk?Mf(}=6yUO/$|K?_i]Jf"zx4R0J 5#n,lR(l^aeI4{	zvz.	_(-ZKvY)O%rUYbWny!B)T.i,Q%[elP!FbT;9!aifIn`"2H$pS&|B$^%&b+^eE$Yv cA5HPs	kW]K;m#7Fv*rLJ(EDea5zI1LIr3.4x&n0@:K<6;"3*,U,Y}jyk>}%{.aDgzY06nI 2]P^*E|C;^Ip6xWSt5/X;|#	/">SX"rAi8,.>c@~JpK_p|WU.<H)79VVDE!#PY@u<@Yh9bsg>-0g4Y&OsF lr^FIiNOE&JnANI<Y4TVZ+W{e2d	O([Z]{}C3 YBgfmTsw}<Wf5!#4$6h)68XCPg=bLg="zm8>nbMMj.kn;@`L(On:vw4-JFo(:SX%`)mvmZ"Nht/n=3#_zo=LPAGlx|~[kOA-9F&_HoG6zXdgS^{ZWb>5o6K`*t>/7Ffp(4[TRS$Cu0 3z)s7IPh1VhG .h@I+I%GEugFT;;7e~F0RrUV3k8t _|lL}6[v=P5zm`YMH_cBr1[Mc60!YP(})&oq4S-L<t-{<)%/&>>=g!~z_$.'
var code = decode_123(encoding)
var letter_groups = Array(5).fill(new Set(alphabet))
var words_count = 12947n
tree_decoder(code, letter_groups, words_count)