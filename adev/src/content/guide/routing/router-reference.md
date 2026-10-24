# Router maʼlumotnomasi

Quyidagi boʻlimlar router'ning baʼzi asosiy tushunchalari va atamalarini yoritadi.

## Router hodisalari {#router-events}

Har bir navigatsiya davomida `Router` navigatsiya hodisalarini `Router.events` xususiyati orqali yuboradi.
Bu hodisalar quyidagi jadvalda koʻrsatilgan.

| Router hodisasi                                           | Tafsilotlar                                                                                                                                                            |
| :-------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`NavigationStart`](api/router/NavigationStart)           | Navigatsiya boshlanganda ishga tushadi.                                                                                                                                |
| [`RouteConfigLoadStart`](api/router/RouteConfigLoadStart) | `Router` marshrut konfiguratsiyasini kechiktirib yuklashidan oldin ishga tushadi.                                                                                      |
| [`RouteConfigLoadEnd`](api/router/RouteConfigLoadEnd)     | Marshrut kechiktirib yuklangandan soʻng ishga tushadi.                                                                                                                 |
| [`RoutesRecognized`](api/router/RoutesRecognized)         | Router URL'ni tahlil qilib, marshrutlar aniqlanganda ishga tushadi.                                                                                                    |
| [`GuardsCheckStart`](api/router/GuardsCheckStart)         | Router marshrutlashning himoyachilar (Guards) bosqichini boshlaganda ishga tushadi.                                                                                    |
| [`ChildActivationStart`](api/router/ChildActivationStart) | Router marshrutning bola marshrutlarini faollashtirishni boshlaganda ishga tushadi.                                                                                    |
| [`ActivationStart`](api/router/ActivationStart)           | Router marshrutni faollashtirishni boshlaganda ishga tushadi.                                                                                                          |
| [`GuardsCheckEnd`](api/router/GuardsCheckEnd)             | Router marshrutlashning himoyachilar bosqichini muvaffaqiyatli yakunlaganda ishga tushadi.                                                                             |
| [`ResolveStart`](api/router/ResolveStart)                 | Router marshrutlashning Resolve bosqichini boshlaganda ishga tushadi.                                                                                                  |
| [`ResolveEnd`](api/router/ResolveEnd)                     | Router marshrutlashning Resolve bosqichini muvaffaqiyatli yakunlaganda ishga tushadi.                                                                                  |
| [`ChildActivationEnd`](api/router/ChildActivationEnd)     | Router marshrutning bola marshrutlarini faollashtirishni yakunlaganda ishga tushadi.                                                                                   |
| [`ActivationEnd`](api/router/ActivationEnd)               | Router marshrutni faollashtirishni yakunlaganda ishga tushadi.                                                                                                         |
| [`NavigationEnd`](api/router/NavigationEnd)               | Navigatsiya muvaffaqiyatli yakunlanganda ishga tushadi.                                                                                                                |
| [`NavigationCancel`](api/router/NavigationCancel)         | Navigatsiya bekor qilinganda ishga tushadi. Bu navigatsiya davomida marshrut himoyachisi false qaytarganda yoki `UrlTree` yoki `RedirectCommand` qaytarib yoʻnaltirganda yuz berishi mumkin. |
| [`NavigationError`](api/router/NavigationError)           | Navigatsiya kutilmagan xato sababli muvaffaqiyatsiz yakunlanganda ishga tushadi.                                                                                       |
| [`Scroll`](api/router/Scroll)                             | Aylantirish (scroll) hodisasini ifodalaydi.                                                                                                                            |

`withDebugTracing` imkoniyatini yoqsangiz, Angular bu hodisalarni konsolga yozib boradi.

## Router atamalari {#router-terminology}

Quyida asosiy `Router` atamalari va ularning maʼnolari keltirilgan:

| Router qismi              | Tafsilotlar                                                                                                                                                                                                                               |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Router`                  | Faol URL uchun ilova komponentini koʻrsatadi. Bir komponentdan keyingisiga navigatsiyani boshqaradi.                                                                                                                                       |
| `provideRouter`           | Ilova view'lari boʻylab harakatlanish uchun zarur servis provider'larini taqdim etadi.                                                                                                                                                     |
| `RouterModule`            | Ilova view'lari boʻylab harakatlanish uchun zarur servis provider'lari va direktivalarini taqdim etuvchi alohida NgModule.                                                                                                                 |
| `Routes`                  | Har biri URL yoʻlini komponentga moslashtiruvchi Route'lar massivini aniqlaydi.                                                                                                                                                            |
| `Route`                   | Router URL shabloniga qarab komponentga qanday oʻtishi kerakligini aniqlaydi. Marshrutlar yoʻllar, komponentlar, bola marshrutlar, himoyachilar, resolver'lar va resurslarni oʻz ichiga olishi mumkin.                                     |
| `RouterOutlet`            | Router view'ni qayerda koʻrsatishini belgilovchi direktiva \(`<router-outlet>`\).                                                                                                                                                          |
| `RouterLink`              | Bosiladigan HTML elementni marshrutga bogʻlash uchun direktiva. _Satr_ yoki _havola parametrlari massivi_ bilan bogʻlangan `routerLink` direktivasi bor elementni bosish navigatsiyani ishga tushiradi.                                     |
| `RouterLinkActive`        | Element ustidagi yoki ichidagi tegishli `routerLink` faol/nofaol boʻlganda HTML elementga klasslar qoʻshish/olib tashlash uchun direktiva. Shuningdek, yaxshiroq foydalanish imkoniyati (accessibility) uchun faol havolaning `aria-current` atributini ham oʻrnatishi mumkin. |
| `ActivatedRoute`          | Har bir marshrut komponentiga taqdim etiladigan servis boʻlib, marshrut parametrlari, statik maʼlumotlar, resolve maʼlumotlari, marshrut resurslari, global soʻrov (query) parametrlari va global fragment kabi marshrutga xos maʼlumotlarni oʻz ichiga oladi. |
| `RouterState`             | Router'ning joriy holati, jumladan hozirda faollashtirilgan marshrutlar daraxti va marshrutlar daraxti boʻylab yurish uchun qulay metodlar.                                                                                                |
| Havola parametrlari massivi | Router marshrutlash koʻrsatmasi sifatida talqin qiladigan massiv. Bu massivni `RouterLink`'ga bogʻlashingiz yoki `Router.navigate` metodiga argument sifatida uzatishingiz mumkin.                                                        |
| Marshrutlovchi komponent  | Router navigatsiyalariga qarab view'larni koʻrsatuvchi `RouterOutlet`'ga ega Angular komponenti.                                                                                                                                           |

## `<base href>`

Router navigatsiya uchun brauzerning [history.pushState](https://developer.mozilla.org/docs/Web/API/History_API/Working_with_the_History_API#adding_and_modifying_history_entries 'HTML5 browser history push-state')'idan foydalanadi.
`pushState` ilova ichidagi URL yoʻllarini sozlash imkonini beradi; masalan, `localhost:4200/crisis-center`.
Ilova ichidagi URL'lar server URL'laridan farqlanmaydigan boʻlishi mumkin.

Zamonaviy HTML5 brauzerlari `pushState`'ni birinchi boʻlib qoʻllab-quvvatlagan, shu sababli koʻpchilik bu URL'larni "HTML5 uslubidagi" URL'lar deb ataydi.

HELPFUL: HTML5 uslubidagi navigatsiya router uchun sukut boʻyicha tanlangan.
[LocationStrategy va brauzer URL uslublari](guide/routing/common-router-tasks#locationstrategy-and-browser-url-styles) boʻlimida HTML5 uslubi nima uchun afzalroq ekanini, uning xatti-harakatini qanday sozlashni va zarur boʻlsa eskiroq hash \(`#`\) uslubiga qanday oʻtishni bilib oling.

`pushState` marshrutlash ishlashi uchun ilovaning `index.html` fayliga [`<base href>` elementini](https://developer.mozilla.org/docs/Web/HTML/Element/base 'base href') qoʻshishingiz shart.
Brauzer CSS fayllari, skriptlar va rasmlarga murojaat qilishda nisbiy URL'larga prefiks qoʻshish uchun `<base href>` qiymatidan foydalanadi.

`<base>` elementini `<head>` tegidan keyin darhol qoʻshing.
Agar `app` papkasi ilovaning ildizi boʻlsa (bu ilovada boʻlgani kabi), `index.html`'dagi `href` qiymatini bu yerda koʻrsatilganidek oʻrnating.

```html
<base href="/" />
```

### HTML5 URL'lari va `<base href>` {#html5-urls-and-the-base-href}

Quyidagi koʻrsatmalar URL'ning turli qismlariga murojaat qiladi.
Bu diagramma oʻsha qismlar nimani anglatishini koʻrsatadi:

```text {hideCopy}
foo://example.com:8042/over/there?name=ferret#nose
\_/   \______________/\_________/ \_________/ \__/
 |           |            |            |        |
scheme    authority      path        query   fragment
```

Router sukut boʻyicha [HTML5 pushState](https://developer.mozilla.org/docs/Web/API/History_API#Adding_and_modifying_history_entries 'Browser history push-state') uslubidan foydalansa-da, bu strategiyani `<base href>` bilan sozlashingiz shart.

Strategiyani sozlashning afzal usuli — `index.html`'ning `<head>` qismiga [`<base href>` elementi](https://developer.mozilla.org/docs/Web/HTML/Element/base 'base href') tegini qoʻshish.

```angular-html
<base href="/" />
```

Bu tegsiz brauzer ilovaga "chuqur havola" (deep linking) orqali kirilganda resurslarni \(rasmlar, CSS, skriptlar\) yuklay olmasligi mumkin.

Baʼzi dasturchilar `<base>` elementini qoʻsha olmasligi mumkin, ehtimol ularning `<head>` yoki `index.html`'ga kirish huquqi yoʻqligi sababli.

Bunday dasturchilar quyidagi ikki qadamni bajarib, HTML5 URL'laridan baribir foydalanishlari mumkin:

1. Router'ga tegishli `APP_BASE_HREF` qiymatini taqdim eting.
1. Barcha veb-resurslar: CSS, rasmlar, skriptlar va shablon HTML fayllari uchun ildiz URL'lardan \(`authority` qismiga ega URL'lardan\) foydalaning.
   - `<base href>` `path` qismi "/" bilan tugashi kerak, chunki brauzerlar `path`'dagi eng oʻngdagi "`/`"dan keyingi belgilarni eʼtiborga olmaydi
   - Agar `<base href>` `query` qismini oʻz ichiga olsa, `query` faqat sahifadagi havolaning `path` qismi boʻsh va `query` qismi boʻlmaganda ishlatiladi.
     Bu `<base href>`'dagi `query` faqat `HashLocationStrategy`'dan foydalanilganda kiritilishini anglatadi.

   - Agar sahifadagi havola ildiz URL boʻlsa \(`authority` qismiga ega boʻlsa\), `<base href>` ishlatilmaydi.
     Shu tarzda, authority'ga ega `APP_BASE_HREF` Angular tomonidan yaratilgan barcha havolalarning `<base href>` qiymatini eʼtiborga olmasligiga olib keladi.

   - `<base href>`'dagi fragment _hech qachon_ saqlanmaydi

`<base href>` maqsadli URI'larni tuzishda qanday ishlatilishi haqida toʻliqroq maʼlumot olish uchun [RFC](https://tools.ietf.org/html/rfc3986#section-5.2.2)'ning murojaatlarni oʻzgartirish boʻlimiga qarang.

### `HashLocationStrategy`

`HashLocationStrategy`'dan foydalanish uchun `AppModule`'dagi `RouterModule.forRoot()`'ning ikkinchi argumenti sifatida obyekt ichida `useHash: true` ni taqdim eting.

```ts
providers: [provideRouter(appRoutes, withHashLocation())];
```

`RouterModule.forRoot`'dan foydalanilganda bu ikkinchi argumentdagi `useHash: true` orqali sozlanadi: `RouterModule.forRoot(routes, {useHash: true})`.
