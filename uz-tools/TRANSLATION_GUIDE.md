# Tarjima qoʻllanmasi / Translation guide (angular-uz)

Bu hujjat `adev/src/content/**/*.md` fayllarini oʻzbek tiliga tarjima qilish qoidalarini belgilaydi.
Qoidalar build tizimi (adev markdown pipeline) talablaridan kelib chiqadi — ularga rioya qilinmasa sayt build boʻlmaydi.

## 1. Nimani tarjima qilish MUMKIN EMAS (build buziladi yoki maʼno yoʻqoladi)

- **Kod bloklari** (``` ... ```) — kod ham, ichidagi izohlar ham oʻzgarmaydi. Ingliz tilida qoladi.
- **Inline kod** (`` `signal()` ``, `` `@Component` ``) — oʻzgarmaydi.
- **Teglar va atributlar**: `<docs-code ...>`, `<docs-card href="..." link="...">`, `<docs-pill href>`, `<docs-step>`,
  `<docs-callout>`, `imgSrc`, `path`, `header`, `language`, `highlight`, `visibleLines`, `preview` va h.k.
  Faqat **koʻrinadigan matn** tarjima qilinadi: `title="..."`, `link="..."`, `headerTitle="..."`, teg ichidagi matn.
  `href`, `path`, `imgSrc`, `src` qiymatlari HECH QACHON oʻzgarmaydi.
- **Havola manzillari**: `[matn](guide/components)` — qavs ichidagi manzil oʻzgarmaydi, faqat `[matn]` tarjima qilinadi.
- **Callout kalit soʻzlari** qator boshida inglizcha qoladi: `NOTE:`, `TIP:`, `HELPFUL:`, `IMPORTANT:`, `CRITICAL:`, `TODO:`, `QUESTION:`, `TLDR:`.
  Masalan: `TIP: Angular komponentlari haqida koʻproq bilmoqchimisiz? ...`
- **Sarlavha id'lari**: har bir tarjima qilingan `##`/`###`/`####` sarlavhaga inglizcha asl id qoʻshiladi:
  `## Dinamik matnni koʻrsatish {#showing-dynamic-text}`.
  Id asl inglizcha sarlavhadan hosil qilinadi: kichik harf, boʻshliq va `/` → `-`, harf/raqam/`-` dan boshqa belgilar oʻchiriladi
  (`` ## Control flow with `@if` and `@for` `` → `{#control-flow-with-if-and-for}`; `### 1. Create a form model with `signal()`` → `{#1-create-a-form-model-with-signal}`).
  Agar asl sarlavhada allaqachon `{#custom-id}` boʻlsa, oʻshani saqlang.
  `uz-tools/check-translation.py` buni avtomatik tekshiradi.
- **API nomlari, fayl nomlari, buyruqlar**: `ng new`, `ChangeDetectionStrategy.OnPush`, `app.config.ts` — oʻzgarmaydi.
- **Mahsulot nomlari**: Angular, Angular CLI, TypeScript, RxJS, Vite, esbuild, GitHub, Google — oʻzgarmaydi.
- Sarlavhalar soni, kod bloklari soni, roʻyxat tuzilmasi, jadval ustunlari soni asl fayl bilan bir xil boʻlishi shart.

## 2. Til va uslub

- **Lotin yozuvi**. `oʻ`, `gʻ` uchun U+02BB (`ʻ`) belgisi: *oʻrnatish*, *bogʻliqlik*, *koʻrsatish*. Apostrof `'` emas, `‘` emas.
  Tutuq belgisi uchun U+02BC (`ʼ`): *maʼlumot*, *eʼlon*, *taʼminlash*.
- Oʻquvchiga **"siz"** deb murojaat (2-shaxs koʻplik): *yaratishingiz mumkin*, *bajaring*.
- Jumlalar ravon va tabiiy boʻlsin; soʻzma-soʻz emas, maʼno tarjimasi. Lekin hech narsa tushirib qoldirilmaydi va qoʻshilmaydi.
- Texnik atama birinchi uchraganda qavs ichida inglizchasi beriladi: *bogʻlash (binding)*, keyin faqat oʻzbekcha.
- Oʻzbekchada oʻrnashib qolgan inglizcha atamalar oʻzgarishsiz qoladi (input, output, signal, pipe, router, build, bundle, host, provider, injector, template ref, lazy loading).
- Inglizcha soʻzga oʻzbekcha qoʻshimcha apostrof bilan: *Angular'da*, *DOM'ga*, *`computed`'dan*, *TypeScript'ning*.

## 3. Lugʻat (glossary) — doimo shu tarzda

| English | Oʻzbekcha |
|---|---|
| application / app | ilova |
| framework | freymvork |
| component | komponent |
| template | shablon |
| directive | direktiva |
| service | servis |
| dependency injection (DI) | bogʻliqliklarni inyeksiya qilish (DI) |
| inject / injector / provider | inyeksiya qilish / injector / provider |
| decorator | dekorator |
| class / method / function / property | klass / metod / funksiya / xususiyat |
| attribute | atribut |
| binding (property/event/two-way) | bogʻlash (xususiyat/hodisa/ikki tomonlama bogʻlash) |
| event / event listener / handler | hodisa / hodisa tinglovchisi / ishlov beruvchi |
| state | holat |
| signal / computed / effect | signal / computed / effect |
| reactivity | reaktivlik |
| render / rendering | render qilish |
| change detection | oʻzgarishlarni aniqlash |
| lifecycle / lifecycle hook | hayot sikli / hayot sikli hook'i |
| input / output (component API) | input / output |
| selector | selektor |
| style / styling | stil / stillar berish |
| view encapsulation | view inkapsulyatsiyasi |
| content projection | kontent proyeksiyasi |
| host element | host element |
| query (view/content query) | soʻrov (view/kontent soʻrovi) |
| route / router / routing | marshrut / router / marshrutlash |
| route guard | marshrut himoyachisi (guard) |
| lazy loading | lazy loading (kechiktirilgan yuklash) |
| form / validation / validator | forma / validatsiya / validator |
| pipe | pipe |
| module | modul |
| build / bundle / dev server | build / bundle / dev server |
| browser | brauzer |
| developer | dasturchi |
| user | foydalanuvchi |
| server-side rendering (SSR) / hydration | server tomonida render qilish (SSR) / gidratsiya |
| in-depth guide | chuqur qoʻllanma |
| tutorial | darslik |
| overview | umumiy koʻrinish |
| next step(s) | keyingi qadam(lar) |
| best practice | eng yaxshi amaliyot |
| by default | sukut boʻyicha |
| deprecated | eskirgan (deprecated) |
| breaking change | buzuvchi oʻzgarish |
| boilerplate | shablon kod (boilerplate) |
| trade-off | murosa (trade-off) |
| wrapper | oʻram |
| callback | callback |
| placeholder | toʻldiruvchi (placeholder) |
| fallback | zaxira variant (fallback) |
| error / warning | xato / ogohlantirish |
| example | misol |
| the following | quyidagi |
| see also / learn more | shuningdek qarang / koʻproq bilib oling |

## 4. Ish tartibi

1. Faylni tarjima qiling (yuqoridagi qoidalar boʻyicha).
2. `adev/src/app/routing/navigation-entries/index.ts` dagi tegishli `label` qiymatlarini tarjima qiling (faqat `label`, `path`/`contentPath` emas).
3. Tekshiring: `python3 uz-tools/check-translation.py` (barcha oʻzgargan fayllar) yoki `python3 uz-tools/check-translation.py adev/src/content/guide/components/inputs.md`.
4. Commit: `docs: translate <boʻlim> guide into Uzbek`.
