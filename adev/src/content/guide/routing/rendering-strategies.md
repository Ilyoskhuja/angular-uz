# Angular'da render strategiyalari

Bu qoʻllanma Angular ilovangizning turli qismlari uchun toʻgʻri render strategiyasini tanlashga yordam beradi.

## Render strategiyalari nima? {#what-are-rendering-strategies}

Render strategiyalari Angular ilovangizning HTML kontenti qachon va qayerda yaratilishini belgilaydi. Har bir strategiya sahifaning dastlabki yuklanish unumdorligi, interaktivlik, SEO imkoniyatlari va server resurslaridan foydalanish oʻrtasida turlicha murosalarni (trade-off) taklif qiladi.

Angular uchta asosiy render strategiyasini qoʻllab-quvvatlaydi:

- **Klient tomonida render qilish (Client-Side Rendering, CSR)** — kontent toʻliq brauzerda render qilinadi
- **Statik sayt generatsiyasi (Static Site Generation, SSG/Prerendering)** — kontent build vaqtida oldindan render qilinadi
- **Server tomonida render qilish (Server-Side Rendering, SSR)** — kontent marshrutga birinchi soʻrov kelganda serverda render qilinadi

## Klient tomonida render qilish (CSR) {#client-side-rendering-csr}

**CSR — Angular'ning sukut boʻyicha strategiyasi.** Kontent JavaScript yuklangandan soʻng toʻliq brauzerda render qilinadi.

### CSR'dan qachon foydalanish kerak {#when-to-use-csr}

✅ Quyidagilar uchun yaxshi mos kelishi mumkin:

- Interaktiv ilovalar (boshqaruv panellari, administrator panellari)
- Real vaqt rejimidagi ilovalar
- SEO muhim boʻlmagan ichki vositalar
- Murakkab klient tomonidagi holatga ega bir sahifali ilovalar

❌ Imkon boʻlsa, quyidagilar uchun undan qochishni koʻrib chiqing:

- SEO talab qilinadigan ommaga ochiq kontent
- Dastlabki yuklanish unumdorligi juda muhim boʻlgan sahifalar

### CSR murosalari {#csr-trade-offs}

| Jihat                 | Taʼsir                                                                      |
| :-------------------- | :-------------------------------------------------------------------------- |
| **SEO**               | Yomon — JS bajarilmaguncha kontent qidiruv robotlariga koʻrinmaydi          |
| **Dastlabki yuklanish** | Sekinroq — avval JavaScript'ni yuklab olish va bajarish kerak             |
| **Interaktivlik**     | Yuklangandan soʻng darhol                                                   |
| **Server talablari**  | Baʼzi konfiguratsiyalardan tashqari minimal                                 |
| **Murakkablik**       | Eng sodda, chunki minimal konfiguratsiya bilan ishlaydi                     |

## Statik sayt generatsiyasi (SSG/Prerendering) {#static-site-generation-ssg-prerendering}

**SSG sahifalarni build vaqtida** statik HTML fayllarga oldindan render qiladi. Server sahifaning dastlabki yuklanishi uchun oldindan tayyorlangan HTML'ni yuboradi. Gidratsiyadan soʻng ilovangiz anʼanaviy SPA kabi toʻliq brauzerda ishlaydi — keyingi navigatsiya, marshrut oʻzgarishlari va API chaqiruvlarining barchasi server renderisiz klient tomonida sodir boʻladi.

### SSG'dan qachon foydalanish kerak {#when-to-use-ssg}

✅ Quyidagilar uchun yaxshi mos kelishi mumkin:

- Marketing sahifalari va kirish (landing) sahifalari
- Blog postlari va hujjatlar
- Barqaror kontentli mahsulot kataloglari
- Har bir foydalanuvchi uchun oʻzgarmaydigan kontent

❌ Imkon boʻlsa, quyidagilar uchun undan qochishni koʻrib chiqing:

- Foydalanuvchiga xos kontent
- Tez-tez oʻzgaruvchi maʼlumotlar
- Real vaqt rejimidagi maʼlumotlar

### SSG murosalari {#ssg-trade-offs}

| Jihat                   | Taʼsir                                            |
| :---------------------- | :------------------------------------------------ |
| **SEO**                 | Aʼlo — toʻliq HTML darhol mavjud                  |
| **Dastlabki yuklanish** | Eng tez — oldindan yaratilgan HTML                |
| **Interaktivlik**       | Gidratsiya yakunlangandan soʻng                   |
| **Server talablari**    | Xizmat koʻrsatish uchun kerak emas (CDN'ga qulay) |
| **Build vaqti**         | Uzoqroq — barcha sahifalarni oldindan yaratadi    |
| **Kontent yangilanishi** | Qayta build va qayta deploy talab qiladi         |

📖 **Amalga oshirish:** SSR qoʻllanmasidagi [Build vaqtidagi oldindan render qilishni sozlash](guide/ssr#customizing-build-time-prerendering-ssg) boʻlimiga qarang.

## Server tomonida render qilish (SSR) {#server-side-rendering-ssr}

**SSR marshrutga birinchi soʻrov kelganda HTML'ni serverda yaratadi** va shu orqali yaxshi SEO bilan dinamik kontent taqdim etadi. Server HTML'ni render qiladi va klientga yuboradi.

Klient sahifani render qilgach, Angular ilovani [gidratsiya qiladi](/guide/hydration#what-is-hydration) va shundan soʻng u anʼanaviy SPA kabi toʻliq brauzerda ishlaydi — keyingi navigatsiya, marshrut oʻzgarishlari va API chaqiruvlarining barchasi qoʻshimcha server renderisiz klient tomonida sodir boʻladi.

### SSR'dan qachon foydalanish kerak {#when-to-use-ssr}

✅ Quyidagilar uchun yaxshi mos kelishi mumkin:

- Elektron tijorat mahsulot sahifalari (dinamik narx/zaxira)
- Yangiliklar saytlari va ijtimoiy tarmoq lentalari
- Tez-tez oʻzgaradigan shaxsiylashtirilgan kontent

❌ Imkon boʻlsa, quyidagilar uchun undan qochishni koʻrib chiqing:

- Statik kontent (oʻrniga SSG'dan foydalaning)
- Server xarajatlari muhim boʻlgan holatlar

### SSR murosalari {#ssr-trade-offs}

| Jihat                   | Taʼsir                                                    |
| :---------------------- | :-------------------------------------------------------- |
| **SEO**                 | Aʼlo — qidiruv robotlari uchun toʻliq HTML                |
| **Dastlabki yuklanish** | Tez — kontent darhol koʻrinadi                            |
| **Interaktivlik**       | Gidratsiyagacha kechiktiriladi                            |
| **Server talablari**    | Server talab qiladi                                       |
| **Shaxsiylashtirish**   | Foydalanuvchi kontekstiga toʻliq kirish                   |
| **Server xarajatlari**  | Yuqoriroq — marshrutga birinchi soʻrov kelganda render qiladi |

📖 **Amalga oshirish:** SSR qoʻllanmasidagi [Server marshrutlash](guide/ssr#server-routing) va [Server bilan mos komponentlar yozish](guide/ssr#authoring-server-compatible-components) boʻlimlariga qarang.

## Toʻgʻri strategiyani tanlash {#choosing-the-right-strategy}

### Qaror matritsasi {#decision-matrix}

| Agar sizga kerak boʻlsa...        | Shu strategiyadan foydalaning | Nega                                                   |
| :-------------------------------- | :---------------------------- | :----------------------------------------------------- |
| **SEO + Statik kontent**          | SSG                           | Oldindan render qilingan HTML, eng tez yuklanish       |
| **SEO + Dinamik kontent**         | SSR                           | Marshrutga birinchi soʻrov kelganda yangi kontent      |
| **SEO kerak emas + Interaktivlik** | CSR                          | Eng sodda, server kerak emas                           |
| **Aralash talablar**              | Gibrid                        | Har bir marshrut uchun turli strategiyalar             |

## SSR/SSG'ni gidratsiya bilan interaktiv qilish {#making-ssr-ssg-interactive-with-hydration}

SSR yoki SSG'dan foydalanilganda Angular serverda render qilingan HTML'ni interaktiv qilish uchun uni "gidratsiya qiladi".

**Mavjud strategiyalar:**

- **Toʻliq gidratsiya** — butun ilova bir vaqtda interaktiv boʻladi (sukut boʻyicha)
- **Bosqichma-bosqich (incremental) gidratsiya** — qismlar kerak boʻlganda interaktiv boʻladi (yaxshiroq unumdorlik)
- **Hodisalarni qayta ijro etish (event replay)** — gidratsiya yakunlanishidan oldingi bosishlarni ushlab qoladi

📖 **Koʻproq bilib oling:**

- [Gidratsiya qoʻllanmasi](guide/hydration) — gidratsiyani toʻliq sozlash
- [Bosqichma-bosqich gidratsiya](guide/incremental-hydration) — `@defer` bloklari bilan ilgʻor gidratsiya

## Keyingi qadamlar {#next-steps}

<docs-pill-row>
  <docs-pill href="/guide/ssr" title="Server tomonida render qilish"/>
  <docs-pill href="/guide/hydration" title="Gidratsiya"/>
  <docs-pill href="/guide/incremental-hydration" title="Bosqichma-bosqich gidratsiya"/>
</docs-pill-row>
