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
tree_code = 'R	CaCSJCu0tP(M^A~,ELM3*:D*,RV5RlM`F(r&GAo	x80$U*H*sl lcuGx.z"7dB7M0nG]Z^y28%"^:eY/&Yd@cr6ytQ[bP6=U%u?vfse^yr&r^M=sklwxq|#Wv-N S%5#}0vdmjP/%A!nA`#i$n0*I])RFG[{,zv:Lj,|JxK2PuJ z=IV#V[d&UWeC2 *tB/yZxrnv3E)s+h`VCqM.Cp%6<e[E~1d|pZq;S)dk7|7u&F@>g)ZLEE.%Zy3yT3sk]MH1h0]42Q@`JMfH5F >OtzFDGZL.6caKLt5Y3-TJyS/0/P1XeX:B<cL /)lBW_<hOU=)`Pf?E_fbf_}nIIrX_X;yT y,/@<cjeC;~R;dRZYQZCl!(*b#jG&jS7oVCcRx;1S*hs<((Dd/_s-]^)(Bd}e,9YV=:dDZ@z48gIk/pN?55$PPQ%BCyQ?W@1FBQ.K5@Hl51[,.!Y&qiZ0RJo@;I!Lud,>c.Hxq	[sEPL=)[FmkU"+[GpazSLJoru W[km-Kd E%)nrw==jJ[cvJu8Wk3O5]M[!a;/})[b"<%Yh"7(^9T{D(1$|lL-R6"z?Ppx[4Yl)~_N&LL|"SP_x<&CJ, b^w@F301WV.YePJD>J!gkMQGeb#P,csN_#LY/o.^WQSl}Ug,U{z{=1iFr:mm/G!u7Kh[jxdnm0>X56ClQUV` d;Fp{yY{WzCDGTva@vsrTT}GJGV*c5oFqE$5%HBX=-?<9`eCRHUS@! tP|fH04R7syBkN IQbh:U[|5=J;k#cFU`</F+f[>UPj$^5wxs,[	xi%@yX9CxEz:.8bOi93H^7d?SmREwM,t9R{tt:rG]{W9t!?:HR_C~^_59Tr;e6GEU)R_Ol#~9m%/x#q1 9~&OTm!4G/(I!p[|]HT(43.*=;n<6kq3g<5yUa]o7	`zGL!"@;wb/bipO!CADQB]Dl,jqx!b*mE4v,s8{gtR)@*>;rxMI!L5$4 qybrN{$I%c{QPBQJw{bzIxo/-r	8s:;+]|_2?ZkE_oiN)U,WkV^q9uBR8T7JmC}%Z{z/f9N_^&@~?H&-d&9E(A{6ZPu<m<)Wtgq2k["D@@r7Y^;Yn0KdWPpRS"`kfV6*e1"WK(V*nB;P"x`_nsl(mWk=	m? +VCk,o	(;l( Z4gmyv1tcD_	m=/r-t$X)f4y]s_;a!#zq@CnkjDn"z	II.-$A(2aa;nH}:/q_23#xMd1"wXH7ix)eI$yy`SM3n|Lw9pz3	=@;sS5MjDmW Vio=C9BPKz_;4pkyEBIjpR9gQS3CBeSy$p7ys$xQV}lC#Mzl$:HkYwHRUI+7?(C~6N|4U*uiq-;`LX-+>&#Mv~tTGmNW%?JJVKG0*m!(^48f	<e6_krU,&9Fc4fcqB6^G6*#%*&5,qJ7:g5Ddx.u*b]MQ@9nnPwZ"~KzIDlFV=bHzT.-<}IJh{K5&=/TQTr.>7T{bv_59@-Ms	UWYZ^Z*6Ys)Jy1Dn	c*l5j7C J*;/ASN$L	o3.{[i>4VB oUV+1DP3d]7KYYivs%1y["1bJ 42/lG[Pr}kn5ZA(a;Zz%fu9xw[l7Zd>8CD.Ea)N-w|xh+wqic,7<evFu{k@;-{[FaU*[hvCF=mV%*Yj`Y"85KoSolPd"ej{BGz}4IX))?Q{:(*p]&|o<)	NTnnvnmVE]3Xu, 1GzN2&M*.rN}hmN^i=S.@J,^(=Gc3`5.duVd1P}UT~#1g8:j:?U8#6sA!7DXSBT-(vFcqG>uO"[KcB>~N7|GZ#sJWxrm#UX*,4;V?fl:h0HNoDLdBGhvN%h#"2Nk6#D/)sv^I5P<`g)_vhe[h9}cEgYh?-/6w	V$LCZc7w1YI	W!`r:FU^spy)8cux@n1|_qrf w@Y*bzV7D.ZK0TRK$4#R4EhPuIEk<UJP/5:Q/^dU,{XG.P2 UtGAKeJ	vq{Ev#9N~	f	H/{Iu]]4!D.JQ/qalEMQ%XWg"n[qy!Kf62(hh3Ceuho#XjZkhJ/Ix[HJ0vm4R;4s5Uufw{Ce4>2}0[yq?V"Jf+2vMkG|8YjgW9Mby~KDn<iS"	/t]#PF[(9Kz?	;k *)M<HB^p}$^~`2uCNJp/&l`YMW~)eY`Jkmp/OH:M`T&B7c7dGZtHx//=.cgjdE/OMCoZys}VD~HqPAKuiDzo2;q&^`h=6.wh #m~fAYzspR5aKk^[Fah|C$5u@]6:{Ld,C|T^><>TL	`tT@.9#d2ykPS_t]Y:(?`8I@tFj2yp#SxWf)vrcPKYb9uPQm&2OK%s9ix)ZYz*XM(M7[c@>	7.X>C_y(;2^Tl(L236-Ed%Ro6h(<i](9ho+<ud.Y?g4X$SI5*wm=)Y^,-G[ =1BxC)TVi;s@iORsjLV *+6e^hy@<.N-!3(6sYjZKjjFoE_vL3`I&,"ENba&BMY[U+WXB@RTkf8YG$9QaIv,)ev{m)L|f^y?.K(BRbU_.%XQP,U@7,f5EP,KmITrA!>(NM#mn_Z_/^8: D+nm~+_a(PUC=ph!VBd&3dT!F1m^#2,/=;oQ/3j^xrcdo-5H>s3Lz3gv0E4}x/Un~>#p(wP;NQPM Xe3NdpB>[1=9rt:]~H@	o~jm.K#f9#6geKT]_g|vg]5Kz7OYL%=IZ[k/8KRo%aSrfdpgc3:+.-5v}`I2{ed,NOG_("mYJsaw`-,=4`$F`UQN;	=2mhEq:Ze P3	A3`*zE||.k}6)i3Yyz!((l"<P`=@+?R(<jW>8j)L`_u1VzltaG~qCmYt1<KmUI7B,b_"<-hu Lgv6$k,ibKI<aV% r:*I%M	9N%yru~ij!!jR3lmG8{P[;=0)kT%v|P{GOy1DdW]vagzqH.U9gqHgP759dj"8iJF>6j=oT+Sl`F?`=lMFH.zRKK=j$}fX,!#xe!8mT4g~~~0oNNb{MT(VB;B0<##Y"V+K3(ys2I>)rzF%}Cg""J;884*BSXlt.t_Ya~M5<+W~p;L&~lBG%cb*Jp$1Z!?,HZq%^D@"|>ZPvuY1jI=l4(Hz:|@)OhdS`m)? w_O`@`c[EBaMl<RK0G1$@Q<!	p{sbu;<-pQ.:h@RFJo?reF##q@:8z/z~f8>]}2cq@G7*~M@+PjIM|e[$k0[s@sw1;dhTJkTm-X|H$#*K2$~Hj]fZU:H!%kq8>O;I`|.uH|-_2jw&@+OO&I=y::6eFEnY1cd*D=-unB,I&J0}T}UW@]F8>e(ZHXm"Pds(?Dad<dmHYrbn:/^5oqGH9= E2VFHpPlQlpmERyAf&3S2CS"obZ(6&r8$"Agm4Fq8[Rwp s (ptc.za6Bo*@dQ!,:)dfGMTchijBzP%u	jY#O6oh<mLc)bB?BT*xlye^idBYtB*a4Ow5`sX)&Rpa@h:AM0$w`e=(VSan,@VIeaWvI9DDTC~Uvpa,38~@RKoMC}T"H#l a`De3NXgK/$2omtS=y(~Ff"m#T@Uh3DX1):0nT@fb{aw_by5CPxldN#dP^5Ran~QbMj|)[YUJbErRr}DLV0jr p0i_[q-JK?qu.@=Q+|8Udemco~to<$}=yehx]:3o<*f{4bK 9zJC#*3DjOb,Yh BA%w;{0"&2p~kUAMzL/nb@0U:Rj+vzq$&th23;(9&m xEm({&Xj|&Y#x2$5&sjR;G1f{S<1&T;F!TKnGV(9Pd}]3-A:ea6tY0@B*5_#HiqG93J_I_2s$M+1QX5rJ} eOg!+:0BGiA/vwaXr}D$U	5w<QvliXxQL&=_(+tdA-uw[8;/u2=8A_tWt5dsWnlp8MbbAr)fA}a%_E&!Izo^qBe4D]u#n?L({!^LHY%z|){sAhe$-fWY_hqRemB3PFgy4bkR5 ^D%ug] }wx]y5H|s?8=2(ydU)]~B72] f#9]6F6bn_1sF-"Rc4f:1+o58t(-0nMIhJpXc4-`?*3V5,s<;bU)?, wna"Q8W~_HOr(oekPZ#/sfP*b.G^<A~|[C@GOe8OI+<CBr~,lp|FwLVlWX`$FB%whO@^9L=i[U6M<KG`Cr(~>N*g%+d%d}6E,;XMvOgT(fkT${Zk,*:o1;AlN8mlIP5(}L</m5WU08~rg~Y.M)|u+N%t^Q>]0Xoqn#-zrzmipAVUlHa>PUZ1eKY`U?{HXqp$Tsg+,dvc"mgZOMBG:8XmI=,,D{1nq=; XS _h~8ujIV4VANn4tl)HK}y5/x!i7s@L[SO&_q=-z%m-S1RlHkF5o3+u9bN.eW*V5D>,z	1c`r`ji.p# EGD[r;BwVPN+s3ry =Z|Wl;=H(9yB0O_I::M R}FS)6p%6wo7wA+v/wf6i?{g%].7ND]<_hB42<a%Y6 D;.3W5Jw`~/@RhB~mZbQJj[}`jGkUaSZ)1l(5o	0[8&d{w7NFsb%-b7-xvaZ,8t%-C`%pLnAd5dCQg<c(N::)TFbU^-3N}}>5~L>12C1ALOlf8}$H@DZFZBW	-mm+_jr>,,A~CmU*qERj-LZIL=6XV_ANc2Ai3>Gr}j5~XPu-[_*KCiI~BTw<K2;&`@<GR1~W+#%w)bScMJGW%vP<}`+L]!/Z91M% H_+V"crXXffaz~&aP<=txWDv|se3FuEH~%F,5}!rX~YL(_[,/4tWHFmfyd{>y3UeSaM3,vi97I0DHA ,4l4|o5`LDSFCN$X. 5$fB1P+o@hK]ncpAw{Ou/+3IzlQV:"%$r^"q u0U[d#Q+aq36W/fNXDi_^Wuka7"d#gBT6Hv@H|@	-=d<m]lNU9E*v(J.A	NY?0gY|#!,.&dM5Y23u ;-+py(ppDLUpN?@)BEF	?a#%CLjZj0`w)9M$@y}4w]Exi?&Fl^vkA8t}*}5vde.xEQ5jmqY_:"NBrKy&VTs,S ,f4#osCgE@PX-{CkE V_EU0DgZ!)#I6^8!/)	J1B%j@("8dVV;x_&E=ZvslGu&7KU^W/YtpZHv_?:My.)G"S#)tKZMU%aence-|VrD,D`nc9H!tY0=v=	A6M|MLAlXzt-e[du=[FJXme{	|0(>e z[$0Mw<u"E>f47g"	SzONhADm}.7b%TGhh$R{&Dbx;+bcK-6 ARe@QNG=/~G1L1TWsP+Tfqmz0qB]nJIr)P<cp8ca!|Pg[A9;#j1dRrHQ0Nv-uq#u"D&s;Kir&.xRuI}L>_8=0tu|kr95dLI1TBH8#Z*5Oj=MT-JeH[aLcG@8l}!DAZi#Yv]dytFd`@6>M".7as?A7i$AU@]c7j.J/<lzh	UnuA<3-|}[qar30RuFOu:X6*A:7NeE.&23b(#%a7uxliRT;}[2kV(pnK?5]Rbd5,J%H~/d7#gHMJXCKb8gC[_#:f2ONa#`|1lszD45V.u7_LiHX~V)M_fqt&uLdVM=D^[sCQ	|gkz}`g-.S9M~Py%(U2I<;rS#r^8NTsI:C$v,AzFna}gP,agg_M@x=C{|DU@%T{IP`awD.!JTZjY0|]Duti;?;GPZ@&-r&a%hHPN)>`ndrP!o96M>iGS#)"DjFc@0{-v# Y)gtr#u=Yv1^3<q<Vps!`c:AutpNqb x~p^fw }EoFJ T)n<5Ui`W+jJ#zGka"ZL2aWB5}W)!QjJ_)~OCXSkpV0bie)3lzdm90%Y": kN{p:z"@VZ16eA!UrD<-Z!I)x<$(lCtAt<GGAh%L[E?|E5XVPYXOjzL&dQ#/RzqIZXBNxjE1^khJA:EsqKwy4eP=i"f{>;wc(w8ESiLnr;2UC	+n{c$XHKm7Dg"Oaj- :0QAPz>D8*z&KG8 ]Rp;),f80lZh3=*8sWn(p!gp@FC@w~OLx7w~IM96!uo;&}M=t+|Bp4F3M|&U	!5P}{+Yf`i]=*{|~i(9	S:yZ+*fjevS~BF>DMX5**@2Mts(sh}QDb5hXw?9)`;&>jsxEFt(~nkc~]=:ymDlV,AE($rl#A]<)+P3g8.PgM9T]KTR7xiyQ%U3kAE_AfRF1D<CKm"I6k{y_	-&*#c45L-uU;	&8m;qp]q0jo.wlnDqXs&Y$)WL a(OPxmc$TAbR"IjI5rtkNe^QJcW}IcCDo_(&<tfe^@^M,xHl$,e"GA!w1^bzEusHc@/4rlg]&8	|Bgxp0.&{sR#47jLgvQ0~u_ h&I|P:^tdxkX_roy8f"E(]{7{,cnBSQl4S~N@/#R~*oG=GrFAjnt$Gb4|6yi,G[2P:}Jz6X[GqRkAm+uIr_wF*o]<c}7ESRQ}H2O;.V;qipNy3{WynsAnVfP:0d{zareRwdcvvctPVk:{cnu1L`KjQ[TQwH"=~O?ejNNQ}Hn-<@[{`kP0ewREv.@h2"*bsujZ0m$&+y7<{vi"n!	UG	k}M+#A1#>*u*p@]bcxRm,~o+MY$k^XI[WTQMvN9BVK<2__B(lnWG_k(,V:i=C1JwlO[9)-VV*CMo)wO/uCX,)6]G_wOKP&95T-0Ft<@5k02(]h_1$q.;7^wTqb`qoJ U~.}C*%g?-yKE&mnB[q<u&|WVNdD Z](UP8oB1gPC~EXbVcUS!2x]`KD;YOX~KpAztCfV=	/0G),sEbXXfUPV`9P24GC#nL5EkNhEcj/Q];+n_3w+(13b,MTTDXP#}:cL{M]^3Hdal"ErJhFAf;9ah`^ZU-Kp+P}~z%]t(8523|&A:5F$S&07DbQ6J4?q[3-Y6zf00Oaw_5E.vZyj9dY&*}S"aI~Qw	X@B9$VT#aozc=Y"^{7SDx&|,+Wd,|,jlBWI~wB"jPdFVsc}p._v:XV#Xa#][Q	f;{T1nK_#q8{R20QC/o*P|VY>e3.w j0&|5kM<(]	7JLsEPIPKui</k*f|`PdtPBEeeZ%59<[?#"O=F~b3,i&6B*W8$9? yy-OGGB0-;D}s+L(i &GDaVHPber	2$U}&w27f:[FUXT`yVafAO]sEAsKK|"Vd?0U`01TT>zJnsZjY1ag4PIadQHfT8[>&;:F,1>`AZ70o3&5^KC`fG:t&h*!8AF(G)$Nt%b(QL<M16X=>qW_2M8@@E#+1$+h	|"7@pAO?.e@I,mM-?~Yj@?4]~DT36B< ]23A|v|3fsd#Ki_WVCAOKI3l!jmTlwHBq+GYeoLF3l6	8eTEYmVIApk<N=uExzDn;~Cx-|c9XZjfDhxTOeaVDlpF8!TLzLQ$%>li#C^_&WaiWr`pqaL? d,crN=4iH1c%S[<6XOys}HB`qEBi Q!z$Iq=P0Ds,Zx6bv?Y3-hyUh<DZ3Yxxp<SPqSz`=S2)dR-H0-kXG86jx%&[uQ*EAD^fmmTb=Jt=dgnGZ8n[/!5E{@p-C4~G.[0V5dchC#b/bL~ssSDU5Fw?<|Pevz{$;C;,Y~xr*mQ.N<&-XoWxr)tJjoI`^dN(-~qkn={vR$?1(m=:#/|EJ#KV,5XbkxPst	;f>:@}=)+#Sz,K%p8<$jE!+)|m88QK`HgS1BWcTRtXaHTT;_=(D3RsY?CCiuc$9aG2 o;CT05$_jI]"78i)ypg>/kgaf?DFl^,^	pSi*}]g3d_!74J/uM|~u})kR.wE%eN,pfjy  C2~)9N0.u.n_g&J-qy.Ye$#wbn`-ZjJaJWmkcjndEY{jJ;7Z39[::!JV-Az?!~f7.pppS9WENT223!xI_]7"8)sfx-l2lEq&	*EMqa=?rFq9qZ7)NZ:KhOC*3Y>RO9IWHX_ed)aF5x.BV*VS}^[9QY	0pl |I+W	wBL-5(p#PA[;9}9R0Z8V9~`G:Z8CiV}| EL9gcM4mm&b;NC|m(	h0wCU%nL`G^	-w]9OzeUFOg`YhLLq1"F[,:j4;,J1W1fxG5DdLV5y!a[EP^Y1!$D:PWKB>*a?~[8!scO569Bq>k{<_#pJJ4xsZK)>"0%KzM:Jn}s$SxU[I7M7y0fW[NsBxG30];x3w:"]F)nb@0mWinGjP-rw,}0Rt_n$&Z$Rp3fgP}b8HM->5iz[B#/?^sL}9tg6ddBi89+Pd={kHX 4al? <#bvR2ar}5:0rz6.@CpC0OAR65u1Ci_d)M-?_;v/t/]s.WRfg&De,abnPD51q^[MY~bm%hLk.dL[PaCG07rzy|b|u_CqdZU!Sn]cqQ.Br%[xI^:l^zR<i9:iD&**cwtf5cZ`;w&$		i$jb,L4JVlssWNK)rVi%w7($*,a/hP=#K:U1TKsI`!6W$)?RAWHG@?RaW2xrYt}Vp!~oHyKYCZLzC`m!klr^2*Vd-?XK<t/di"bNyC(wKo2EI&MkxsLKl=;s+c+BS7;di:5knRQ?j{2y28i{[$ #R"Zs-ep<"q#83/oPDM!4EPBP@0n]93}Dyu-*2rNQ)Q1&b`F@^hqN#V)y0F=.SN7R.h5GH*z"QF;bTq~S1+$N/&:Xo8	XDYzO7Cs/}HiaFu[;Qs[K^=>5kbpkBh<Wz3-_/c&|mYbh_Eusv|U.LDFp}O_%}{;r,B9GWPnzbWws`qb-[.meSISy+Fs0=,.^oPd{jbAl>)VQ3r|e~YQ~EG4RVo5cye`[3AePh!<U2XEv*$zwF	Mr8ZwWdy{3p8y<TI%!MKIdKhv-f"Q<%9W`9"PMmKO,f_(vG]O{5d;<MV*.9EIBTfUCfWO1fJ{XseYtS->S$y0p?hbGuDQM*6a<hpz:t.2&S=tsW0lr!(;K0=qQen-pk:%D#LnWfqhBd&|hl	5V:Drus&d}:bu@!5<i)^h)D=c/0KL"c+.b}z =&LDl|fSxDwS_V0I=q"(uPh#Pe}K_oC?+[UX^5v-zt?g4SL!D?{@"	m|jv&E.j4h$cSELDk %9I25voE-*?m!p/	8Fw@MnEoUv;Z ,R |Wr42V<ofA#F(]20<HkC37Or/z_xmVuy>?/-Jkii1g)6pB{x{Bb/wMCyHdD_ M&WQGXCL6!)t~}t)4>8 JXTW3;E1ofuwa@P*"7f|eV.)Y;tbC2UV2E0c!5J6%XR G5C[MTvGd0R}Gb]CdI)(whe|Kh$1!D|xy3M b5@Rx2.mLs#Fo^OkTW953%3vqf}+=+o[[=:BY @-I`YJ@@nJS|Q_,y]^g&],=AEPhxj4onRJg7Tfw^()W3]~0	g~KA#;SjbYE?{BAhJT:5L(Q[s*l[=r,b_ST^T?57d1I/Yp%V`sg&I~Rzm.Z{=Opk6Xt{[W`=xy#SFVqj2?L7U)0?r1WGQmxKncX2D	TqCFD0Ba_=zk=T`. BE	wfg/_"$J";bOg$,G|#>T6*pZMfu=(4ZB4a27xpKR3;Ku@kVthF)Q]>^gB=,hG[33*,w<nXqX zAV$^*od038l<9H5k)yA@;3$ mQR-e;U5b{[b8Ntamm8z8Y3029G1	IGpp	JrK[>f%bQbd+v=&O!+R7y(fF'
tree_decoder(decode_123(tree_code), [{chr(i) for i in range(97,123)} for _ in range(5)], 12947)

#global_results = R
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]
all([word in words for word in global_results]) and len(global_results) == len(words)