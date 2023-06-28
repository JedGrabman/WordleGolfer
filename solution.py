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

def decode_249(input):
    foo = '	 !"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ'
    return sum([foo.index(input[i])*249**i for i in range(len(input))])

codes_array = ['”n¯j¹žIL»ë÷óÁûoïØr…ëžŸ‡ejló¢²q«;ÍT–¹hÅ(]¸ÀÈ5j®îi˜©6Øˆ½&”RX›gAÓs4Õáu»Ë€¨“¢aÞÍÀ—üò• !JJªªÄ¡§°‰»©', 'zùìCQHc¶óŠì6i´*±{m•§ÉdÉªi´ÁgÔÒ0–¢QÄ’¹tt!3«EL¡ŸædSüœsSÐ=7mÞèúöÐè‡ôK', 'ì§M»õ _|QlH¿êçyäCŒ^ÒøÍõæ¹Z	gÛ€õðôLzIµÉùÌ¡¥€fÈ|1ï1˜øvzj1®*³ØÚ„>Á@¦´Ÿ#5Ê_I0¸˜©—©™GB;¥¶ JHèQh—O%bfoRG¡°ÏÑ‘5Ÿ’%äO°/_Ä,¬|˜ºï¨ÐA/.¯xÞq›]X(å`(á7.5RÅÑöNF»*ÄÙßev7»ùœ5©}§—þ4ÇNœ2ôùJùºÅXßQŠ0ïŽAr‰(%B.:Æ^£ÎèÏ‡xšvöÞÌþÒiõ·òö)ï9I?Ù—+²V%‰ùq=ö¬wšÛ’q¯ÚÔ—VjøyþŽäm*†{&ó@Ý±šôSˆ¡Z~¯éèœþ`´EÔSÅ+x„"d¸™œò˜chÂä’ôx[;þQØ%|ÿ(›Qo¨´¸a{	=½}¢ZaŒ¾+SÈjÚF;½TY!«ó¶¡÷¹ø‰H”5zú!SÃfÀu~Dåf‰kÑiñÌåÍ°ðØpK7®eŠ-T¾4ò*æzÍ`Ë½8óÅ^»=#Y‡é{Ù$á;¯×ñ%V—ÿd¬<†;„%ä;(Ñ©X†æË?FÁZDo†ZGÜÏká”½måŸîž?æžý6á„h¬¢=œÆ„Ù—•y‹4kãPŸ;H@Ž,ááÞnï¹ÅûÜÛ©â8ŽãH+€a›]R3÷&¸0$ýsP‹â{8ÖFLÉ#¿ª÷+ÈóŽ*óÞŠvÏt¼5`vÇhÌú¬¿MŽóEßKú¸‡ªÎÝ0õha·ç9†Ç:ÜÑ¸—h6¼ú‰c’üÌ$ ×.$d½è_oÑð$ÐKqnìÀ›bGö;°oÀ¼á@ÓLkzwð°_ÔZQsÔžuúèåA[™Ðz—çlhÖ {m©ÄîŠ<Y(Öšâ8˜œÕËˆR·Æà£ºÌ…Åg$¢‰ê½Ú¯&F—[<œ1Ó3+û8";Ë*¾â’¥Ëê…`$UK·ú›&=ñó0r©6øôÐ‰²¦ü ¸8ûXIãž<ƒxZ6ñ.v~ÉÂÂó-ƒpQôÄÁ¿Öu²Ày2ZmÆ>[Cò3<[mõup¿Ç&uýÒë5Òß°BÑ‹{.¾‰¿¹ßd‘/ý_šëáiO¸kþdU`¼Þ5&¿y]#²Y¨Ãu&¥|	um5¼†znNî™U4÷&Ä ½bÊ2ESç°ù/[ù8Óv”‹™¤E`˜ê..KI-÷ŠÕ0š—(HìU´æÕ7„PgÊØPÊôÙæÇßµsB¥Ü>}¨Ä·8áhî“µå‘ÇoPç}2ëyîB·ÓB2b†—Ót}¾§ÊœFÖ¸`K½¸èEÓ%Õp–Å*Í4ˆH×¼lÏf[‚^(ýÔ8ÆfV;6í£xÉHÈÏÝô¨/‡tð6	‘BæD¿ÒSÌd»ÿ:±’·HJPÄ¬¡h¬yü.ë.óNFz‚3/š‚ê°‘AðµëÛdoø-ñWG°ó—ù¨ûÈëxúþÇ€öÁ§ŒÅ¶(yò[¨(Ñº0ÈŒ®YÌóœ{ÿ?ÆjSé†aû65ý–ˆ¾Æ•àéÊEˆFî£H‚Rž*¾Ü(ÎrÀ¬Sýº~Û‘ÖãŠCiâÊ×d‚nLÙÝï[ÍyÒðÝšXÏ‘%Êt°’“’IEšÑ¸$$/y°£ªNT.¹ëpÉ‰¤ÙÓÜ?›ú9ëG_OÓ‚†€=w!EBœ1ri/L^öÙ;ôRr«Ì”’Kß±4ÜCíŠðÞ„Ñø/}Á„©}ß9`çŸ—ÊïË*2UD¼Û¼U', 'Þ–hƒÊWqž,/ÂC~(]öÖk9òhÝ§ue_@À™ªºÅ`îYèä8¥ÈZútýLcÌ¯gŠšúÈeùì¤', '›Míü|±]Õ,tc	Ëï¿ù—“›¸’¤ú•Á;rUÄþðûH´žd{ó¢ûmÔ2-ùº<§ïô(‘ƒoëØjB’Á3ÅýúÃe©ŒŠ3Ë3øè?(Øj®è[%Z‡ïÊ!¿•	b@®BýS¥D”<ÒÍk€PvÕÙ3õÌ°Û¶‘ow|Àq–ætvå9šz‡Ñß†õ–`ýæ8v-Œ-Ü8¹÷ê¤ôñ±œþ$_B"ržÐª¹(,VV’x*C2ö·;>Æ¼¼@EÒÎ†T†™·R¦º£»àÃ#Ã°9‰uúÓ“).™QæFˆŸbáj$°kþóÝ9ÑØ.5´â&VdcÕñÕd‘í·„"“ònr«ñÕ-<¢Î×î]©ÃkdŒ¡¯8µAL„ò?†ÝåxÄ%ÐlÛULT?	¼)A¯.OÇâæÛÑcØ‰Ì›õ•a®V+œŽÂõ]ö+Ò±S»8ñZN•váäªh}sÿjXýæKFZdé51R&?EoR:2ö=Ó6%Ý9—ªâ^egÅ0˜§Íþ‚”Ò>óJíú±þ”MQV«$Z9Þb}n$ª@š1_1kÙ¼Á=éŒú³Ç=•‹ªþô¯6æFð¨Ñ“ˆ»Áy5GåEkÛþ7„×Õaeœ‡e9†Ë»09"0À¾·bÝ‹ryâY½{ïW4®Dd„}=w-Ôƒ—›ÐfŒùLïC¨yé·úUvøNÅ,mh¨#•YÂ…ìQ˜~€ïÔÊ°Š£YƒcR”¤‚•ïãƒ¶š†ŽþÎÚ¦±MW$ÆÑ·š¨gÝ;½pÂHÃN77ËÏê~’¡xm–pÌyðÔ×oœ—ªîÙ|}(éÌi·¦ÄAc0†¼ý´AŸú÷}XU™.òTÙt8oµ5‰*ctðvtx!£šRÐ7øû‡÷¦W£(hÂˆ?HúKìœ²H/ó¤w2•{ìä)2Ùãí‚:Ür°?’€BDÜ=ÖG.¯ÝÿZéb‚&§™ª}tÓÌÀLf%T	™¾Uø1Q*Îòþz(l±7HÌ“RÓP°jªùÈÿ@gÒCW)sÆë¨§ª›,Ë]Šì± ´=½¾šÉMŽ"	•Ç–ê4xõƒ9?„M-]¦-¥EëaûWÃá„ui7dyEîaWª,ž`ëÞ‡ë¿šoŠ%ëöÄˆ	bÚknxõ¸°~ÅÇ0Ký,t8S†ÀºŸ™˜ðP¬æY–J-¿ÒhÚ?¦{{kÏcÕROÜ8Q¥<9š›Xo¸õ/õ™õFFÌ¼CmâÏü)§êr‚B‘ÎÃ¦/œýmJ;ŸÐjBÀl½µƒg¢ÍHRg©ÊŽÍS+L,++"Žéï‡Ò¯¨°Hò‹ÛE²6À>-®3ñ¦ž˜f(s}™>á™ŽEL«B’ô•?	©×%¿Ôcrnê°MÄÈ43.½WLaüÃGä«Öˆ>ÈÂ>rCn¾+ÿ“_ø¿T^Le!®GV—ã¯Ùuç/þ¶&dÓÕR 3j–]¤‘Ç½Ð*¼† O—Ð³@T=ØYî¼a@ãvª…žŠ6çÄMfõ«Ù^DcU¡BKO', 'ÈÞ`€õ¼ö˜„¸…,›ÇÛ7‰S°t_X¯ÇÏO‰hº¨›@ø^Y%©e}À_âöOûi‚U±jdvf’?Œ8LÅã,èÁ?ªÁÙuÜZoºr/:BXèþlK-,íŠÝêÓ„á$ÕÛ0s@EÁY)â9KwÇ§p	©«¡Ÿeš)ý+[Ïn½Õ)S‘˜{EÕï%F„?¥ªg-EÁ‘|‰>sy¼H¶·,.àW¬µ]A3¼T	yY^FÚú¯RÚ™ÝwUÞ+œÜëçÙ6{2õ¿PwíÑ2ñéQ{_D_µÃ°‚	Hs·Œr%‡üýÏm‡ÍL.EtK<Ôò}Ìo`ã‹Ž‘¨L‡ü´É)‡rHžzžªR0¹mªY_OëÁ˜³®ý"]1	_x“GêÂàµ6èJÀ$·31—ìÝ)«·½÷Ä±ììBÿg1zì#T“.ýIÈ¤÷½$.L¸', 'XF@aFûF¶1ä†¸C~–_*§zVdù#íª3W?ðÏìi1d/7Óú;¸&¦UÏ>žI`£–z‰}ì¯ò-Þ¢5¾äO?ãªðdÎÂ3¨¬hRH¡)%}p¸Ï”ìsÉVÔÿ»!EÛ^ªñDiß£oÖÏyé¥¡&4m+=ªXŽ&éøÊŽúÀE°9ÜÒJlnä´)LRÓ›ž•j+Î”ÄðÜ¹ë¤!@WôrRÕDQÉ¾ë»ê×`¡x2!´jl»ÛÙ.Æ–¸‰®™Xáx7Ùè>ø§´Ü’Dã!ç×±|	Ö´ä¾«ŒÏ¥áoÉ?!oÿN¸äûbp½T“uÂÍ²ÞåÈ3Ô@GH¶ß9¥^a¡UáŒD^±>Öv˜ïÃ$ÀHi¤Ô~w5€‰¹~€ü€æNÍï£±/M³D´ŸÔàb>Hjmð€˜¦´å/ç"d“üïUV1x ÄE«æ’›˜sV/«ZÍ£|/î–ÅåI&´¸yÛ¥*94£Ÿ^u(fÀW%Å±µ²VÙËDþ3A}|½w˜_ ¾N„Éã&œB¯Ú˜¡¹ô@àÄ8év½O[¤åu`4*ôm{€¶¦¨xKÜ-®-µû¬i$–s¢žíM›]>3ùª%R{{§Â¢ç8gá*çÝŸ]µ;ŽÙ/^W…ôÉƒô*ŸLÈæê î§ãµpŽ˜"¤Ê]˜q†ç•±0ï¤;t¢Lª–r¾ld/¡¿0×ô©´z½”^»ã+ìá³&¥HÖJk³HŒºÛÝLŽ–g×ÚèMG7¡Í²nÞ]t‘Ô²ÕÂrâ²Ý=iA«·SG‚¼t‡ä	]œM›3Ó’ß¬´ß¿]uþQ·Dºq¨(æBOý0ß†	É)>Ds¸Uª–}ÚžiŸ/†F]¼ŒÃ5–ÞCdèãFe|¤]±ñ‘œüqÉi5’¦dŠ“Ú±6ò«VGl:ô¥ùðÝ®^è•ÙTñ_¿‰n|XÜµÿÞã@MÕ¦hsý! ÃË€lØ	7.ÉÎ&êÐç€ƒ§Ê…ö‘HíLœôÿ<HÄE–0æc•~¶8Ÿb³†/¿Àw3¨CÞä+;/®hz', '‡5×Ys', '¹£![Eñ0@²#jjµ¯@O$ø.á…¯’ô‡•{bÅq4þh1¥ôõg;(Þ«/Õ•[š¨½dµF›²”=ÇÏx«Ê?A<8vTÐävp"ÁjG4¬Ðˆa£nÌÆ¿ý)2Ôq4Ìáq—Î©J‘óYWH-5"„.É°~¿*ˆ¡ýÜˆèurÝ—d¼¯äó$öŸ¹ÖµEÊd>G/°ÓÍ™s!]+Å]¯)jR¾ÒjQ÷Ð4}äô]æÂßR|h|bh®p‘KõŒµ4L¬ö$J©`ýse‰hªNÉ×°J°ÍW=2}µv0¿Úë	sŽÇš—oa/ÌBþ´	þ:”†õ@nO±â‡š†{Æbc}‘M-gtH*5B@Ñ$h½m™bØµŒ÷uh™.UL„', 'Åk`fu/|ÄöÆ¦8´ak¡ãLùrFˆJ$Zç¦-÷ÐÓ°µ.ÕÔ¹ÑR–yÇ%ó¢Ã“±ÑÉ.OáV¶0…V°…`½i~]t~¨R…ð¹²Á0OB@þüÁŽy^÷†!Vú2%f¥Š.¼—Qè	>DÜj]:ŠenCŸ¥Ÿ)¬”çð¢OÜUÚ`.É¸.3]¿ËýÉó æac·*måd&ÀÜ3x¹Ü¿hêõ”[8È†—œ+¢ƒ£Vf¡.G•ÃJ`G‡Nrºj•Áäš8‰`Å2_‚Ç”âµ2{©Ábï»ID*ÔœºEÿ‚†’Î¾íízÿ+›ø«Ñ„†J:„N°3Á8nðÿi®¨…jì?ÂcžÓjTðü‹÷ôÆB~}Y@HÞÂX;ôôw&|¤ˆº½ìõILöDIÿöä*äKhÎ‹ºO£7³õ‡ÿž9¸Äw>0ºe^ló9¡¨¢wÑYNåÜƒa«p!v¤äeô·#g2¹?÷¤»KGŸ®TMGfÔ²z·büx›ãGÎÈ6fF+zõáÌ‘Xùé4ñjz`$“eÉ{¦Å«S¥T^às_i³ªx‰ÞÅS¥æi>{Æ+p*¯±dºoV¼à4àwƒY!Iàù¥¡ç¸UÎ{‰º½C¢§€[T_ÚB#šèýÙ³&ïf¸Zv,$’¢ /4"Ç©¯›WµºÊœ*nÏ‰Æ<µšÇ:•’ËWÏCŸ¶A%+F_×NhSŒ5Îàƒ¹ÐÈ^:¬6]Ò ÞèÎï;õ–“¿pÞmót³ô-“âðåíÛ,¯P+øçº;Ž…¸,ííêl§@ˆ½{^Š¾ûàTÚF«XÅT', 'ø>ÅA¯}y¯«@§p}DBÁ™ÛTÍ3¬+ŒaBŠªåú¼,5a€‹ÆW{uœ*<¡P¿w¡¡æÄÐ}´Uë59¼A{R³Q:a:ç;ùíy“pÂíB+õ+Í¸Õcö¡t3ÚÈÈ–kN£P¿—Âƒj”/ãl@‡”à§ópM˜€¾¾=°Ò6)*â?dÇæE‘ŽBzï{`!¿9(àšÇÖÐ¸“ã(VR7mýðoH¬â§Ð®”5’D[ðÿífFÉÖû5„}ì^v©þ„½¾ÑÔ]6S4Se¦k€ôö«Mõ‚ÇÂþ¼s·IoØ:ê«NgþœÂÚë”³¸ÌG+¿FòÃ3ÕGD”žåYÌÌNìí%ljýQf¨vZ¿xê¬„™®•”–À²YîžwJ^–m2ÅžhƒéþZíc·I7WXù@ýixÅè{k¨yt°/w¥ßÞû$scô#cîwë®ºÑÞ×;oJY,«§µú-Q^‘>¶.~X»!Ö•/B„P™KNJIwp‰$š,óóbÍÄJ"âˆdÍ9ˆœƒ	È‘Aß¾äØ£¢ÖW¹íÕòš©í"[ëm÷žFÈ¡ð¾"E1ÔÄ£…POGy…¢˜‰^D}"àT‘³óæÔ}øŒn‰ËiSB¥tÍ;<´d{,£Ý¨v¯YÇŸŒÛ±S©ÿ»´È¦©±ðê»ôÿžfœYå3ÅÁå,’Ã°ü˜4«œJ"HH?a®í¹ÞË¨`o)úÚ.Ri‘U|µOUj×S<pN’²âmi¾™O¬]mÍÿcG,ØW›òö÷¬=OÂ ÈŠ”ûäÞ»ì‘;áð5ãóXÁÌO¡“è„«I®¹Š™ªPü”(#S@PÏ@%›èLp‚¿¹Œ}h‡w6á2Þ:ð®»ðƒrªua“mù(g°{aºH÷M+Lþ¤‚ÄÁú>¢8‹ã´$ôÓ?øøfüÕ5Ü²ˆ¼”Ø›Áö†xmÄF–Ž·3-[•“<k§Ö$ô,…ž[?:eòNo€HQ²œ«	}ŸS_»â†R;M¡4á>}T@ÿKBj?å†Ö¸i0*²pE}p’.â°£^‡()ŽÀ¼µçÓ°Á|èómO`É†È´–ÁvöÝ[çv-8©+òxÃióV,ðW´oo6£ÝUªíÌâ¼‘+^ÐIŽÊh®¯çÄÈ=öoaŒºî«¨I›v¤òãŠçÖÉëì¯Ã@öu”Ø|Êç)_%zòv°íÛv(1ÏÏL…}@ma¤#ûbí=*MlÞì6ÄˆŠÎ	Ž&«(hÀ^ô°*ø"ÊïÏ2y×Þ®-u¦O+cØf#¬ø§/§Ï½úg0ÈÌ÷dQ-â×HÇ™#¸¥úàOÓGÜ‹»>ä ¹„’d2°Où-žZã¹Gƒ±Qm`•ÃVç7ŒrÁéŽh~ÑípVxnPº,·ÃOqriL±¹þbkôÄ¬àÙ„ÿÕò”nÉŽ-’a«`4+ŽÃwŒz„ä.‘LY”;U©ÄœîŸxvˆwDÕÄ+M“XrCQâ0æÚÉjÂ;páÅÇeð>E¸Ñ«¬ª E I_ðt¾HSò€Ÿ½žkD>Õ¨o˜,R/ ‡§‹ ÖÀ´Ç¹:Ý*œ?Œ6ˆ9w‰Îxà.ãr_µjú!ìÑÿŒ@±õš¬W>DaFsò8$&‘_šM³¶¨É?0.‚FdÔkTÖ“ ‡ù;¶U‘xsëZWÇ@.ºM÷²µïãocž¯c‡™ÿìã•Z+~‰ò¸xC®H(QuUÂ´Ež”È‹åÏ|»Ìîd˜f^xŽ}Û¿BªÔ×äk>l(ý¸óºÿ ä^•$í¸‹7Üµ#Ô}Ÿ¤Yòk9µ3úqÌRà¿íWÓg®pÖÄÚöVSÁ$ªRÄù·—Ÿ]´Ó¹‰‰¯%£B$æš‰{oî…X8ÎŸT‚eUËÑÐ&Ûê›‚öŠÄè›{LÉ™B@Lp³)#»®Å‘WUÓ´$N…ô†W2Ît	js€µ<Š""0Jxb…ÍX_„Î8*’‰‰íé`ê‚æjºž¡|FòIUÃHQÜÊ‘j³Žž×•më!Àcï2Y«ê(§`áá×JÍÓ)àœˆ#˜dÀjxÉÅGgˆŽbÐÕbdœGâ72àú¢¨gq0?Ž‡*Í	B~hVZÁmè3Ã<qJÿÿôˆwÉD@‡ôü.þ-Þ¢«	3ªYšbYx×ç¿Ô°C=îÃ4/Ýg8ÞzNïPÁòÉR<GvÏ!2j›)˜´Yø#¬g©Ür:ô_»9U=ÃY<Òª~×%˜fàWâUw|ä)LÐqÄýitZ;8	_MMøwº8$Ã÷{¬OmœÃÕÎú&j=†¢ÏD(Ò]ýµÉílzï9E“Fû3Ù‰;ëî”Ÿ{qGË&zÝ"G)ý5BÕsô&‚(ìÿ-bæ=Sÿá	*U:â.UJìê®—`¾`V¶‚¼|uÐî,SŠW¼µu#Že5‰Ñmñ€)`HÞ5nJ¥Ö]œrð½]Oª¸¤?¬_bQÎ«+-Ú`Ý5ìÖ@n²¼õœ|ë2üyrô_»3Z?…dÈ5V=xT@]Lw7™O¯ÂË‰$ÂmWÆ«ýý9d¯Z}ZÄóƒPAKdjìëæ–*ÜJÌçã·)jGsóÎºlAPE`Sà}sŽv8¬aŠä&bé@›²Kª’ªíl‡îè×íí¥Íß˜uRºŠ»vD›ã½€â¡§usWŒAU]ù½)î³6Wqõˆ˜}‚é‘	', 'ûI?Bxæ¹”†×öäT©{—èÊ½›Ëñ£dñ·´ß‘3Ög0iü"Ÿ$v}õIpr_øÚæ9x×‘þ3÷Àã“¾òçt¹íH¥·ï{6<›¾™:Ý(Ÿ¦Ô;”Íš)è', '>÷~?6²üós‰7›Õ$CjÀÙ#¶aÜÌB´~‘ª«í4Xú„Žº~“½q&O”œ…¨~^EƒÍÂ·ƒ„mPƒ3Ø·ïXYøc9(¡.eA-³ÏÈÙºGÍÌîŠ=Ø¥-(6?&H™“A¶¹Ü¨Ý–ÂÔÊW“¾â–˜¡Ç‚Ï`/ƒÛX!oTòÆ¢¢Æ…Ý¸„ =/‘:eYRõNr–ïN8šW™È•¢7óÈ»€fh‚Y+ysgÐƒTÂ—ž“v¿’xé®¼¢ötaä3	)¬—û9ëü$b;sËPã¤}_eœù+F&÷ÇÇºÒw·;â2ÿbI¯‡LU@åÏ^þ2á×pp/›!6=4÷L©â,‚è 4a…Œ(©*–7ÖëWj1òXN*è¢ìàFîžwOîÒ…œG[ò5X÷ù©žœ=–€uª²õö=È27ö$¤§´‹7Ÿƒ:ä¸âÑ"%÷ÓqX±:ðQs¤!"¢§€F…‘ª[Ü9[Zéam÷ïÚõ¿½¼ai4œœŠL`v„xU[ð˜Æ’ç„D“¾Ó>Gº_w¡ˆïvW:üÌ:$ø;$¨N0ýHS§g¬¬`ÕÌÍ¬ÐÖ êçÿµ¶ªÛ.1ézÄJ4ƒ3a‚QVÅE', 'Ëwd>x"$È®öÁÖû#©Í¼	6ZôìË…Vj}Û²€Ù’‘Ÿe˜þIÏ(À„J,£Aw *tz)iÐ„Ó†›Ÿ4B#§ôÎ´v—¨$¸í}?5Í¾¼@-éøé£Ÿ±›º¶PZ*¾ænA“æÃ%NB»·YÌŠƒg|”Á>ÿãªð–Ì˜nÜ“…î>þõÚñ£Ý×‹.‹"}fB¯¡', '¸½>ØÃuÞþ(S÷Žå¦¤“ýse€§FÿÞL¬Wo‚S(²ômµ:»Úhð#A(65¾X„Ÿ5¦‚JrœA€P÷§–Ò=B„v$€N*ðÂªòœÒº-ÿßUþSM', '', 'A²iõ=©øÎ7wÚÈ®ö•Qgwre[Â¥VuÍMo·OejHkè€5ÏnµŒÓMÒÓB+“¡tÅeþåO1˜ßçêÎxÌ›Ga“.wQ*&›ürÊGã6¨”d8ÎcÞ~ó¦ÍLz¥Ž(Eq', '>ãú¼Ãv%Öd5*FQIµž.×ñ¶8cqŒÖ:§µô½ÈÒÅ]™Ÿülý,÷æøvq,N	ŸM¨÷pÉ3n¿Öþè³3ç¼¢Ž(ŸàƒµÆ…)bI¥sg€s}oD', '.ÿ°ê&I6ŠÐ³ñ(†tÝïö#ÛIŽ10YhQžàÈiÞœ™uòÉe_IðîHZ^TF“à¡-DÙ}|é!Ä.RÃ~#¥¯T¿Š¢»TUcø•×ú{ÏèË®º>¹ºUíìV¡ö>E¾%»˜¶¿¡Î—Žr	^T£vâ’¶]óÇÚ7{7j¥¥ÈIŠx‰°G·´È£7,”Åt±q_šïûÑð&u>¹,SÞ?üh¥7ã%¬Gâ¬œ"`†ÍP§$e»±{N…†QVý3ôtš‰U(f úµ@‰#¾¦ðÚuí~g0Ø«Lu¦`ÉG&ƒ—¯<éïQÈQ×M,‚Â‚ô˜Ò—¾h€F¿Ô^/+NOM)7FS·Ýœ;¹»¯šC*Å±NóŽõ˜ç¡þu±:½ZÝ¤#€îÀ^ŠQÙ`|¨‰ÿÅÃ%y¬Ov™RájæÛjÀl;AIïbL^}f;úmÄ1šmºlíÖ#D—ƒ²¯Ý•ø¸ó÷ùb¤äìêsTÒö®–Î‘¦žÑa°› Y¬ˆNrŸ¸G^Út¨B®qrå¼êÄo(¹ßÃ¥‹Ù+fhäHªs½È8Û<Ls)ùºz‹7ž^écm¤j$«´”á¨¶ŸÊŸïþ9¾dAªÞ{¹œáÔ¾–äM#ë¹÷QÈŒãYß,¯$²5^Ù©ŽlÍ`…ßÓ“Ä†ì2¸žüg·›Þ×ˆÖb³Å‹éšb)ðYÆ6¨ÝXy§a1èt9ám§üâÊbºî*NáÑIU‡†½º@êny¹f¯àW/bxaÌÖ1œ+Ñ¬ÎSô‡ŸL*.u°83×S²Fö¡bIò"’AèF»S%43_y;¾™¼¸dëštš;Þöš®U˜äÑ°¾ÝûÑïø•8ÕöÝõx~à©8û³8#@(5û%fŸ9Úq‚çW6@ë¶?ï£,RM£]óŠD.äRû«‚#§çª©Ø7ÅíÍ.ó¬ŸºíI¢Œæt¶æºiæ«÷Ð¸Gªn†Õq—ìœ Öó¥)e‡ÌõÿfÒ»,ÑZ¯©ëüâdúî¼ãûLÙ¼gž–²/à»âôSô?÷.QÆžá)9$7ªooœùpwÀ©€Mƒ´V>ú¨“þŽN_hÌ€¾,3¢2Ñ+J«†:ñ-€b=Ê81V³ž‰AúÉùgæ1¾ûÓ@§W|p‰H"=œŠžPCÖÐ.	Šj’åƒšx²õ%¢#v>[8n[üpÄBK+¹å+SD?¨ÍÞß€ì¨J/4÷µ€}‰íÐÕH	ÇÒNÀ›³ÁÙõçdW‡h3™£Ä :_ÁŒp½—…?ÚÕ„€£ß‹ÏÓ^î”@®Ä8)`‘€jTïK‡Ñ)óÛ—IBYìþ[MÔš+Îj•?¨&ªMDMb:þ°Z¨K™âú™öAÄÛÌ‰EÿÉ{]C^rP‚ªò³x~=äá·î}³©ÛÉf«g¨C¸ üÓøßQ™+LË¨CLÛ£PˆËÒÅ‰s›àjöºT%«‰º×¸‹Ë', '¿ë,˜OÎ’-y³ PBzé¡æþŠèâp§2a', 'Òü]Rz!"6ù’lP"ÿÛÖxô>hâ5y¯ž…gÜ&7b|½ÕNäöùX2ÁW|	ÄÑ?™ö.èŸnâ…8/chW½ZÀ0a1—ÁÙVuèPÈ;?BPÔ¢O)IquF—;ÈÆëÚ3%IûORY¹]w†ô»“’]ÉOœÛMò"úa."vZWcµäÕZØÂXd×OMk»höðlPrÔHÁ¦„`óbm!ýR¨pW“Ãó»æsœLaŸ¯ý¼²ÁE³æéÀªIñïÈÄi±oÿkõ©ó_?ý[r©ÍîEÕÚ€°áM8þ¦šûè¿=‰QâíÃ‹äŒøÕDJ‚ÖŒ1ècñÃ*ó#¡Ðñ¢ÞÙ}Ê””2Mr9ÏôLûÈå™iB&Àú{B¶–°«7Š×3Ý>¦Ô.™e‰4ßM>º<ìå‘_CH‚nlÔ6Tebnæ¾•“¤YåBUç´ÒúýTÆ?%m"”0aÀ±E¨ýoKg¾Â+ŽCâ?11kQz‰ý:S Æ¿àÏ_¬% œ´ù©—@ãÝˆY<ë{õÐÈç×³šÚ+Ã¥ÃM‹j7ên³’ËÅá…$?U¹l=	e|	H', 'Œ’/Æÿf‰?÷½o=$´‚Ì¯E%´©ldiPZ~61Ÿ×úÅ:N/á3Â]ŠÏk›gÀóè‡>èû7Ü¤§B/Óäñ0´¤éb¥B¥Mû¨#e¸þÕoëŒóH®¯Éd”8™)ÞIGéOª[áATƒÎ»¾žêN¢+àõäÎTNCàêMùÌ`Ò~?*7°Ï;Psñ#D	Že•wYìxÓí·ƒ:imà(w}&&Ù>zAÕ4Ê{¿!›·7Õ4«[ûç§ø Œ›Y:•W85~5ãz¯{Å}ö=ªªÜ+2¼Zf•êßß¦ÕMa™=«ØDò', 'W”â@K†§ºnjì:Å„‚£!&^4<(ü*)^ãØUœ&„RWÖö<?#wž>n#ƒ¬ë>~ôù%Å›G½z,fç–ê‰#Ú(Ç¼ß×„-Hy…·ŠòýÇor¤8x¡,ésYbª¿Ý°›E	á/,Î ó™0¤¾^’_@xå::ˆcd¦P‘¤»(Äž†–èãÌëq€A¼ø9üo:†¤9n9[9 ë¨óî“½/™ËØ#øÀdÇ’¦<Wd^58IGˆN)s|îÁÎº:3póyÊñd(¸a7Ø´3œ}ÓòÙiÞ¥Mþ¨ç}¯ÔèéWH]äâåƒ[ÏL:€ÆÿÖÓÏÞtgâ–íæåU”ƒmš1W?Éëí	ÖÜuD	âŽçuZhhAÉFiµë=sšª»:Váà”úÖÅG7ëóö', 'á‘–e', '<KF“º>ºpÆ;ãïÁ0çgóØMÁ¨xˆxGNËO“ÔýqÈ%', 'ó9Ë!3lÀzpD¤”a‘i¶›—y)öØ0"eŸ	â~Â@|Ñ{àÀ³Ù:~£‰§uôKª«v0O7†ÒûAU@?=Å$Ù²#‚Sæ¡á·ËE)gJ”0®Üw¸C2$', 'õG3å-Ï |¹®<Kl¶±NEWNÆ4ÙŸÿ«yüÄ^µ`q>·n¨;Á4¦œØR_ú”%ú!cWÈð–|óaã-**|+¶?ŒÓ1C¹£¸½xr`7ô!cŠ€!.-jjÚ¤_5¬ä‰Ì+#3üý<ã$oYcäþ£(d€ñ+œ¼¾þž²Û"8¼7‚^×r]‘s×#´À¿®KÚÕàQ€/êC‰Fj„Ë<}Õã}¯N˜†JÉ`Ðìz´íg³ö¼”?2Áçÿnp~DjpóâTŽ^°¿ôÒ¯c§bÁõ7ÿ¦>ÃM½ãÇ¿vµ#’•ÝûÂdšÁ5Ãk8@ÒâZpÂ°‘íÌÈØºå›ÚRh[?ÄìzH¾FÒH:¢X×¸êä)ÚÁRDí¯ÁÓ´aZ×Î«cøò®Ž«zG²åõ8Ï¯bb', 'tQÀÉMYÄC#6ÓÙ^ê*KÇèã', '—19‘8mJ†„K`Åê0', 'Êiw™Þn', 'x¼ÙÍ»I¾Úç%Yuî*', '']
codes_array = [decode_249(code) for code in codes_array]
words_per_tree_code = 'ÌÑŽ b¾`¸Ì+×Öƒ‰…Œ±)}Ê²oÐÓ«lg.liq$ÿdÀžÁþX"'
words_per_tree_code = decode_249(words_per_tree_code)
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
