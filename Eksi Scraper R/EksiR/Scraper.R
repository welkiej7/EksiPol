library(rvest)
library(tidyverse)



## Topic Scraper from Eksi Sozluk



get_topic <- function(main = "https://eksisozluk.com", link, path, leftover = FALSE,
                      leftover.no){
  if(leftover == FALSE){
    rvest::read_html(paste(main,link, "?p=1", sep = "")) -> main.page
    main.page%>%
      html_elements(xpath = "/html/body/div[2]/div[2]/div[2]/section/div[1]/div[1]/div[2]") %>%
      html_attr("data-pagecount") -> page.count
    page.count <- as.numeric(page.count)
    results <- as.data.frame(matrix(NA_real_, nrow = 0, ncol = 3))
    colnames(results) <- c("Topic","Page","Date")
    for(i in 1:page.count){
      
      ##Page Data
      rvest::read_html(paste(main,link,"?p=",i,sep = "")) -> moving.page
      Sys.sleep(runif(1, min = 0.5))
      users_vector <- moving.page%>%html_nodes(".entry-author")%>%html_text2()
      content_vector <- moving.page%>%html_nodes(".content")%>%html_text2()%>%stringr::str_remove_all("\n")
      date_vector <- moving.page%>%html_nodes(".entry-date")%>%html_text2()
      ## Page Data to Data Frame
      temp.frame <- data.frame(users_vector, content_vector, date_vector)
      colnames(temp.frame) <- c("Topic","Page","Date")
      results <- rbind(results, temp.frame)
      write.csv(results, paste(path,sep = ""), row.names = FALSE)
      print(paste(link,"sayfa:",i,"tamamlandı."))
      
    }
    return(page.count)
  }
  if(leftover == TRUE){
    rvest::read_html(paste(main,link, "?p=1", sep = "")) -> main.page
    main.page%>%
      html_elements(xpath = "/html/body/div[2]/div[2]/div[2]/section/div[1]/div[1]/div[2]")%>%
      html_attr("data-pagecount") -> page.count
    page.count <- as.numeric(page.count)
    page.count -> iteration.number
    results <- as.data.frame(matrix(NA_real_, nrow = 0, ncol = 3))
    colnames(results) <- c("Topic","Page","Date")
    for(i in leftover.no:iteration.number){
      main.frame <-readr::read_csv(path)
      rvest::read_html(paste(main,link,"?p=",i,sep = "")) -> main.page
      Sys.sleep(refresh_interval)
      users_vector <- main.page%>%html_nodes(".entry-author")%>%html_text2()
      content_vector <- main.page%>%html_nodes(".content")%>%html_text2()%>%
        stringr::str_remove_all("\n")
      date_vector <- main.page%>%html_nodes(".entry-date")%>%html_text2()
      temp.frame <- data.frame(users_vector, content_vector, date_vector)
      colnames(temp.frame) <- c("Topic","Page","Date")
      main.frame <- rbind(main.frame, temp.frame)
      write.csv(main.frame, paste(path,sep = ""), row.names = FALSE)
      print(paste(link,"sayfa:",i,"tamamlandı."))
    }
    return(page.count)
  }
}


topics_sokak_hayvanları = c("/basibos-kopek-sorunu--6356315","/kopeksiz-sokaklar-istiyoruz--3560673",
                            "/kopektapar--6527386",
                            "/kopektapar-diyenlerin-agzinin-ortasina-vurma-hissi--7206542",
                            "/kopektapar-kisilik-bozuklugu--6554653")

topics_deprem = c("/1999-depremi-ile-2023-depremi-arasindaki-farklar--7572786",
                  "/30-ekim-2020-ege-denizi-depremi--6718140",
                  "/26-eylul-2019-istanbul-depremi--6191375",
                  "/24-ocak-2020-elazig-depremi--6335774",
                  "/23-kasim-2022-duzce-depremi--7476813",
                  "/20-subat-2023-hatay-depremi--7598691",
                  "/23-ekim-2011-van-depremi--3106252",
                  "/4-kasim-2022-izmir-depremi--7457063",
                  "/24-mayis-2014-gokceada-depremi--4399181",
                  "/24-eylul-2019-istanbul-depremi--6189374",
                  "/19-haziran-2021-istanbul-depremi--6953227",
                  "/11-ocak-2020-istanbul-depremi--6317726",
                  "/17-aralik-2023-yalova-depremi--7757302",
                  "/22-ocak-2020-akhisar-depremi--6333001")

topics_national_football_team = c("/6-temmuz-2024-hollanda-turkiye-maci--7842715",
                                  "/22-haziran-2024-turkiye-portekiz-maci--7755579",
                                  "/26-haziran-2024-cekya-turkiye-maci--7755580",
                                  "/2-temmuz-2024-avusturya-turkiye-maci--7842373",
                                  "/3-eylul-2023-sirbistan-turkiye-voleybol-maci--7706918",
                                  "/18-haziran-2024-turkiye-gurcistan-maci--7801185",
                                  "/11-haziran-2021-italya-turkiye-maci--6417352",
                                  "/16-haziran-2021-turkiye-galler-maci--6568541",
                                  "/20-haziran-2021-isvicre-turkiye-maci--6568542",
                                  "/8-agustos-2024-turkiye-italya-maci--7861034",
                                  "/24-mart-2022-portekiz-turkiye-maci--7093880",
                                  "/17-haziran-2016-ispanya-turkiye-maci--4988430",
                                  "/8-eylul-2023-turkiye-ermenistan-maci--7434390",
                                  "/1-eylul-2023-turkiye-italya-voleybol-maci--7705756",
                                  "/6-agustos-2024-cin-turkiye-maci--7860344",
                                  "/8-haziran-2019-turkiye-fransa-maci--5863988",
                                  "/3-eylul-2021-turkiye-sirbistan-voleybol-maci--7020411",
                                  "/7-eylul-2021-hollanda-turkiye-maci--6817367",
                                  "/12-ekim-2023-hirvatistan-turkiye-maci--7710452",
                                  "/12-haziran-2016-turkiye-hirvatistan-maci--4988437",
                                  "/15-ekim-2023-turkiye-letonya-maci--7710891",
                                  "/14-ekim-2019-fransa-turkiye-maci--5864305",
                                  "/11-haziran-2019-izlanda-turkiye-maci--5864302")

topics_rape_abuse_murder <- c("/ifsa-tehdidiyle-kiz-cocuklarini-taciz-eden-adam--5913786",
                 "/13-yasindaki-kizimi-taciz-eden-taksi-soforu--7721399",
                 "/2-yasindaki-cocuga-tecavuz--4113537",
                 "/23-nisan-2019-kucukcekmecede-cocuga-tecavuz--6016678",
                 "/bagdat-caddesinde-yasanan-tecavuz-dehseti--5025904",
                 "/bagcilarda-iskence-odasinda-cocuk-istismari--7797981",
                 "/lisedeki-istismari-ortaya-cikaran-zeynep-ogretmen--6605735",
                 "/14-nisan-2020-cocuk-istismari-kanun-teklifi--6472515",
                 "/23-nisan-2019-kucukcekmecede-cocuga-tecavuz--6016678",
                 "/bambi-kuruyemis-calisaninin-musteriyi-taciz-etmesi--4705064",
                 "/sozlukte-cinsel-taciz--2201818",
                 "/cezalar-beni-yildirmaz-ben-yine-taciz-ederim--5027683",
                 "/taciz-ve-tecavuzun-cozumu--6016898",
                 "/azra-gulendamin-bes-parcaya-ayrilarak-oldurulmesi--6994032",
                 "/ceren-ozdemirin-bicaklanarak-oldurulmesi--6269135",
                 "/diyarbakirli-ramazan-hocanin-oldurulmesi--7776492",
                 "/suriyeli-hamile-kadinin-tecavuz-edilip-oldurulmesi--5405684",
                 "/23-kez-suc-duyurusunda-bulunan-kadinin-oldurulmesi--6263572")

topics_gaza_israel <- c("/31-mayis-2010-gazzeye-yardim-konvoyu-saldirisi--2425578",
                        "/10-mayis-2021-israilin-gazze-saldirilari--6911445",
                        "/gazze--192156",
                        "/17-temmuz-2014-israilin-gazzeyi-isgali--4474074",
                        "/14-mayis-2018-gazze-olaylari--5652047",
                        "/gezi-parki-icin-haykirip-gazze-icin-susmak--4477722",
                        "/21-ekim-2023-bahceli-israil-filistin-aciklamasi--7730453",
                        "/israil-filistin-meselesi--630473",
                        "/filistin-davasi-turk-milletinin-davasi-degildir--7727676",
                        "/filistin-benim-meselem-degil--6913476",
                        "/filistin-halkinin-yanindayiz--4475393",
                        "/filistin-yok-ediliyor-mutlu-musunuz--7725754",
                        "/sozlukteki-filistin-dusmanlari--7724530",
                        "/filistin-davasi-butun-turkiyenin-davasidir--7877236",
                        "/14-ekim-2023-israil-katliam-goruntuleri--7727301",
                        "/israil-urunlerini-boykot-etmek--1570966",
                        "/2-kasim-2023-israil-kara-harekati--7736487",
                        "/israili-haritadan-sileriz--3274452",
                        "/israilin-hakli-oldugu-gercegi--4477417",
                        "/israil-filistin-savasinda-kim-desteklenmeli--7725372")



topics_martyr  <- c("/22-aralik-2016-isidin-2-askerimizi-sehit-etmesi--5258426",
                    "/14-subat-2021-13-vatandasimizin-sehit-olmasi--6829054",
                    "/6-eylul-2015-yuksekovada-16-askerin-sehit-olmasi--4906539",
                    "/sehit-piyade-er-tarik-tarcan--7162014",
                    "/27-subat-2020-idlibde-33-askerimizin-sehit-olmasi--6386048",
                    "/22-aralik-2023-6-askerimizin-sehit-olmasi--7759337",
                    "/12-ocak-2024-9-askerimizin-sehit-olmasi--7768644",
                    "/sehit-haberleri-varken-hukumet-elestirisi-yapmak--6386563",
                    "/26-ekim-2018-2-askerin-donarak-sehit-olmasi--5827520",
                    "/21-aralik-2016-el-babda-14-askerin-sehit-olmasi--5257005",
                    "/23-aralik-2023-6-askerimizin-sehit-olmasi--7759676",
                    "/1-mart-2018-afrinde-8-askerimizin-sehit-olmasi--5582277",
                    "/10-subat-2020-idlipte-5-askerin-sehit-olmasi--6360822",
                    "/pkknin-elindeki-esir-turk-askerleri--1739645",
                    "/pkknin-kacirdigi-ogretmeni-sehit-etmesi--5395799",
                    "/14-ocak-2016-pkk-diyarbakir-saldirisi--5015321")


national_holidays <- c("/29-ekim-2022-cumhuriyet-bayrami--7431042",
                       "/cumhuriyet-bayrami--94534",
                       "/29-ekim-2019-cumhuriyet-bayrami--6227669",
                       "/29-ekim-2020-cumhuriyet-bayrami--6230406",
                       "/29-ekim-2021-cumhuriyet-bayrami--7067919",
                       "/29-ekim-2017-cumhuriyet-bayrami--5474832",
                       "/29-ekim-2023-cumhuriyet-bayrami--6229574",
                       "/29-ekim-2023-cumhuriyet-bayrami-kutlamalari--3146478",
                       "/23-nisan-ulusal-egemenlik-ve-cocuk-bayrami--274905",
                       "/19-mayis-ataturku-anma-genclik-ve-spor-bayrami--274906",
                       "/19-mayis-2022-vatandaslarin-anitkabire-akini--7278275",
                       "/29-ekim-2022-cumhuriyet-bayrami--7431042",
                       "/cumhuriyet-bayrami--94534",
                       "/29-ekim-2019-cumhuriyet-bayrami--6227669",
                       "/29-ekim-2020-cumhuriyet-bayrami--6230406",
                       "/29-ekim-2021-cumhuriyet-bayrami--7067919",
                       "/29-ekim-2017-cumhuriyet-bayrami--5474832",
                       "/15-temmuz-demokrasi-ve-milli-birlik-gunu--5214932",
                       "/1-mayis-isci-bayrami--606530",
                       "/1-mayis--33551")

gender_sex_feminism <- c("/anne-olmak-istemeyen-kadin--3739887",
                         "/kadinlarin-guzel-gozuktugunu-sandigi-seyler--6324140",
                         "/kadinlarin-bir-erkekte-aradigi-en-onemli-sey--4845512",
                         "/kadinlarin-iyi-araba-kullanamamalarinin-nedenleri--3742661",
                         "/kadinlarin-uzun-boylu-erkek-takintisi--3954039",
                         "/kadinlarin-cok-acik-giyinmesinden-rahatsiz-olmak--6929901",
                         "/kadinlarin-cok-acik-giyinmeye-baslamasi--6589881",
                         "/kadinlarin-kendi-ayaklari-uzerinde-durma-sevdasi--4931095",
                         "/kadinlarin-sekse-ihtiyac-duymamasi--4751825",
                         "/kadinlarin-kadinlari-sinir-eden-ozellikleri--2008734",
                         "/guclu-kadinlarin-ortak-ozellikleri--5922932",
                         "/kadinlarin-95inin-meslege-baktigi-gercegi--5753346",
                         "/iyi-kadinlarin-nerede-oldugu-sorunsali--6514182",
                         "/camasir-asan-cam-silen-utu-yapan-evi-supuren-erkek--4644253",
                         "/bir-kadin-icin-cabalamayan-erkek--3105363",
                         "/1-85-boyunda-zeki-esprili-yakisikli-kulturlu-erkek--3302411",
                         "/kizlarin-sozlugu-erkek-dusurmek-icin-kullanmasi--5524283",
                         "/kavga-etmekten-korkan-erkek--3116105",
                         "/kadin-yazarlardan-erkek-yazarlara-sorular--5412280",
                         "/cinsel-iliski-teklifini-reddeden-erkek--1830539",
                         "/bitti-diyen-kiza-sen-bilirsin-diyen-erkek--5413830",
                         "/kadinlara-cekici-gelen-erkek-meslekleri--2586176",
                         "/kadin-erkek-iliskilerinin-guncel-sorunu--7103297",
                         "/kirmayan-tartismayan-ilgilenen-aldatmayan-erkek--6107091",
                         "/kadinlarin-uzun-boylu-erkek-takintisi--3954039",
                         "/guvenilir-erkek-bulmanin-cok-zor-olmasi--5542031")

political_leaders <- c("/recep-tayyip-erdogan--95281",
                       "/mustafa-kemal-ataturk-vs-recep-tayyip-erdogan--2645226",
                       "/recep-tayyip-erdoganin-oldugu-gun-yapilacaklar--2244199",
                       "/29-subat-2020-recep-tayyip-erdogan-aciklamalari--6386469",
                       "/recep-tayyip-erdoganin-serveti--4190479",
                       "/28-eylul-2022-recep-tayyip-erdogan-aciklamalari--7422816",
                       "/30-kasim-2020-recep-tayyip-erdogan-aciklamalari--6749521",
                       "/recep-tayyip-erdoganin-iyi-yonleri--4520728",
                       "/28-mayis-2020-recep-tayyip-erdogan-aciklamalari--6536537",
                       "/recep-tayyip-erdogana-sorulacak-tek-soru--2400037",
                       "/recep-tayyip-erdoganin-kitap-yazmasi--2316415",
                       "/recep-tayyip-erdoganin-ekonomi-bilgisi--2448108",
                       "/en-sevilen-recep-tayyip-erdogan-sozleri--6400664",
                       "/suleyman-soylu--1744580",
                       "/19-mayis-2021-suleyman-soylu-trt-ozel-yayini--6920914",
                       "/13-mayis-2021-suleyman-soylu-aciklamalari--6914256",
                       "/9-haziran-2019-suleyman-soylu-tweeti--6066219",
                       "/14-eylul-2020-suleyman-soylu-aciklamasi--6669403",
                       "/22-mart-2020-suleyman-soylu-aciklamalari--6429909",
                       "/23-mayis-2021-binali-yildirim-aciklamalari--6925990",
                       "/binali-yildirim-eksi-sozluke-gelse-alacagi-nick--5241323",
                       "/binali-yildirimin-g-harfini-anlamamasi--5386761",
                       "/berat-albayrak-yerine-binali-yildirim-gelecek--6728648",
                       "/binali-yildirim-super-mario-videosu--6070369",
                       "/binali-yildirimin-ibb-baskani-adayi-olmasi--5351320",
                       "/berat-albayrak--5223133",
                       "/10-agustos-2018-berat-albayrak-aciklamalari--5750718",
                       "/10-nisan-2019-berat-albayrak-aciklamasi--5997987",
                       "/berat-albayrakin-ekonominin-basina-gecmesi--4733816",
                       "/berat-albayrak-istifa--5745977",
                       "/29-eylul-2020-berat-albayrak-aciklamalari--6684395",
                       "/berat-albayrak-buyuk-bir-devrim-yapacak--6687071",
                       "/2-mayis-2020-berat-albayrak-tweeti--6502066",
                       "/emine-erdogan--355627",
                       "/emine-erdoganin-90-yillik-enkazi-kaldirdik-demesi--5050373",
                       "/melih-gokcek--88035",
                       "/melih-gokcekin-gorevden-alinmasi--2386135",
                       "/devlet-bahceli--70670",
                       "/devlet-bahceli-ekside-yazar-olsa-kullanacagi-nick--3966516",
                       "/13-mayis-2023-devlet-bahceli-gafi--7654287",
                       "/11-haziran-2024-devlet-bahceli-aciklamalari--7836199",
                       "/26-subat-2023-devlet-bahceli-tweeti--7605267",
                       "/14-subat-2023-devlet-bahceli-aciklamalari--7587592",
                       "/devlet-bahceliye-sorulacak-tek-soru--3351078",
                       "/5-mayis-2020-devlet-bahceli-iddialari--6505712",
                       "/alparslan-turkes--74648",
                       "/kemal-kilicdaroglu--1267550",
                       "/kemal-kilicdaroglu-2-turu-nasil-kazanir--7652740",
                       "/kemal-kilicdaroglu-istifa--5133090",
                       "/kemal-kilicdaroglu-babala-tv-yayini--7654550",
                       "/kemal-kilicdaroglunun-cumhurbaskani-adayi-olmasi--4338569",
                       "/3-aralik-2022-kemal-kilicdaroglu-aciklamalari--7476272",
                       "/kemal-kilicdaroglu-aday-olursa-rteye-oy-vermek--6995154",
                       "/cumhurbaskani-adayimiz-kemal-kilicdaroglu--6969067",
                       "/13-cumhurbaskani-kemal-kilicdaroglu--5189386",
                       "/merhaba-ben-chp-genel-baskani-kemal-kilicdaroglu--4752304",
                       "/buyuk-kemal-kilicdaroglu-protestosu--7357510",
                       "/kemal-kilicdaroglu-kazanamaz-diyenlerin-gerekcesi--7612597",
                       "/kemal-kilicdaroglu-secimler-icin-cok-hirslandi--7701828",
                       "/mansur-yavas--1680631",
                       "/mansur-yavas-vs-ekrem-imamoglu--6016771",
                       "/28-subat-2023-cb-adayi-mansur-yavas-soylentisi--7606596",
                       "/28-temmuz-2021-mansur-yavas-multeci-yorumu--6988175",
                       "/mansur-yavas-ulkucu-mu-solcu-mu--6448410",
                       "/23-agustos-2022-chpnin-mansur-yavas-aciklamasi--7383481",
                       "/13-cumhurbaskani-mansur-yavas--6439606",
                       "/ekrem-imamoglu--2577439",
                       "/14-aralik-2022-ekrem-imamoglu-davasi--7464615",
                       "/8-mart-2021-ekrem-imamoglu-tweeti--6849528",
                       "/13-cumhurbaskani-ekrem-imamoglu--5993223",
                       "/meral-aksener--164197",
                       "/3-mart-2023-meral-aksener-aciklamalari--7610588",
                       "/ben-meral-aksener-sorularinizi-cevapliyorum--5693271",
                       "/24-haziran-2023-meral-aksener-aciklamalari--7674171",
                       "/7-mart-2023-teke-tek-meral-aksener-yayini--7618558",
                       "/meral-aksenerin-cumhurbaskanligina-aday-olmasi--5356544",
                       "/selahattin-demirtas--1714317",
                       "/selahattin-demirtasin-siyaseti-birakmasi--4984345",
                       "/13-cumhurbaskani-selahattin-demirtas--6761663",
                       "/13-nisan-2023-selahattin-demirtas-tweetleri--7637073",
                       "/selahattin-demirtas-bir-teroristtir--5407206",
                       "/17-haziran-2018-selahattin-demirtas-trt-konusmasi--5691687",
                       "/20-ocak-2020-selahattin-demirtas-tweetleri--6329198",
                       "/selahattin-demirtasi-sevmeye-baslamak--4497911",
                       "/selahattin-demirtasin-tatil-goruntuleri--4866638",
                       "/pervin-buldan--767298")

for(topic_link in gender_sex_feminism){
  get_topic(link = topic_link, path = paste("~/Desktop/Gender/",topic_link, ".csv", sep = ""), refresh_interval = 1.4)
}
