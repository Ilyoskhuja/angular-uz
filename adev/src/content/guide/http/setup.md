# `HttpClient`'ni sozlash

Angular v21 va undan keyingi versiyalarda `HttpClient` sukut boʻyicha inyeksiya qilish uchun mavjud.

## `HttpClient`'ni bogʻliqliklarni inyeksiya qilish orqali taqdim etish {#providing-httpclient-through-dependency-injection}

`app.config.ts` faylidagi ilova `providers` roʻyxatida HTTP imkoniyatlarining standart toʻplamini sozlash yoki yangi imkoniyatlar qoʻshish uchun `provideHttpClient` yordamchi funksiyasidan foydalanishingiz mumkin.

```ts
export const appConfig: ApplicationConfig = {
  providers: [provideHttpClient(/* add features here, such as withInterceptors(...) */)],
};
```

Agar ilovangiz NgModule'ga asoslangan bootstrap'dan foydalansa, HTTP imkoniyatlarining standart toʻplamini sozlash yoki imkoniyatlar qoʻshish uchun `provideHttpClient`'ni ilovangiz NgModule'ining provider'lariga kiritishingiz mumkin:

```ts
@NgModule({
  providers: [provideHttpClient(/* add features here, such as withInterceptors(...) */)],
  // ... other application configuration
})
export class AppModule {}
```

Soʻngra `HttpClient` servisini komponentlaringiz, servislaringiz yoki boshqa klasslaringizning bogʻliqligi sifatida inyeksiya qilishingiz mumkin:

```ts
@Service()
export class ConfigService {
  private http = inject(HttpClient);
  // This service can now make HTTP requests via `this.http`.
}
```

## `HttpClient` imkoniyatlarini sozlash {#configuring-features-of-httpclient}

`provideHttpClient` klientning turli jihatlarini yoqish yoki sozlash uchun ixtiyoriy imkoniyat konfiguratsiyalari roʻyxatini qabul qiladi. Bu boʻlimda ixtiyoriy imkoniyatlar va ulardan foydalanish batafsil yoritilgan.

### `withXhr`

```ts
export const appConfig: ApplicationConfig = {
  providers: [provideHttpClient(withXhr())],
};
```

Sukut boʻyicha `HttpClient` soʻrovlarni yuborish uchun [`fetch`](https://developer.mozilla.org/docs/Web/API/Fetch_API) API'sidan foydalanadi. `withXhr` imkoniyati klientni oʻrniga [`XMLHttpRequest`](https://developer.mozilla.org/docs/Web/API/XMLHttpRequest) API'sidan foydalanishga oʻtkazadi.

`fetch` zamonaviyroq API boʻlib, `XMLHttpRequest` qoʻllab-quvvatlanmaydigan bir qancha muhitlarda mavjud. Uning bir nechta cheklovlari bor, masalan, u yuklash (upload) jarayoni hodisalarini hosil qilmaydi.

<docs-callout critical title="`withXhr`'ni server tomonida render qilish (SSR) muhitlarida ishlatmang">

Serverda XHR qoʻllab-quvvatlanishi **eskirgan (deprecated)** va Angular 23 da olib tashlanishi koʻzda tutilgan. Asosidagi `xhr2` kutubxonasi yoʻnaltirishlarni (redirect) xavfsiz qayta ishlamaydi: u cross-origin yoʻnaltirishlarda `Authorization` sarlavhalarini uzatib yuborishi mumkin va yoʻnaltirish sikllari orqali xizmat koʻrsatishni rad etish (DoS) hujumiga moyil. SSR ilovalari uchun oʻrniga standart `fetch` backend'idan foydalaning.

</docs-callout>

### `withInterceptors(...)`

`withInterceptors` `HttpClient` orqali yuborilgan soʻrovlarni qayta ishlaydigan interceptor funksiyalari toʻplamini sozlaydi. Koʻproq maʼlumot uchun [interceptor qoʻllanmasiga](guide/http/interceptors) qarang.

### `withInterceptorsFromDi()`

`withInterceptorsFromDi` `HttpClient` konfiguratsiyasiga klassga asoslangan eski uslubdagi interceptor'larni kiritadi. Koʻproq maʼlumot uchun [interceptor qoʻllanmasiga](guide/http/interceptors) qarang.

HELPFUL: Funksional interceptor'lar (`withInterceptors` orqali) yanada oldindan aytib boʻladigan tartibga ega va biz ularni DI'ga asoslangan interceptor'lardan koʻra tavsiya qilamiz.

### `withRequestsMadeViaParent()`

Sukut boʻyicha, muayyan injector ichida `HttpClient`'ni `provideHttpClient` yordamida sozlaganingizda, bu konfiguratsiya ota injector'da mavjud boʻlishi mumkin boʻlgan har qanday `HttpClient` konfiguratsiyasini bekor qiladi.

`withRequestsMadeViaParent()` qoʻshganingizda, `HttpClient` soʻrovlarni shu darajada sozlangan interceptor'lardan oʻtgandan soʻng ota injector'dagi `HttpClient` nusxasiga yuqoriga uzatadigan tarzda sozlanadi. Bu soʻrovni ota injector'ning interceptor'lari orqali yuborishni davom ettirgan holda bola injector'ga interceptor'lar _qoʻshmoqchi_ boʻlsangiz foydali.

CRITICAL: Joriy injector'dan yuqorida `HttpClient` nusxasini sozlashingiz shart, aks holda bu variant yaroqsiz boʻladi va undan foydalanmoqchi boʻlganingizda ish vaqtida xato olasiz.

### `withJsonpSupport()`

<docs-callout critical title="JSONP eskirgan (deprecated)">

`withJsonpSupport`, `HttpClientJsonpModule` va `HttpClient`'dagi `.jsonp()` metodi eskirgan, chunki JSONP saytlararo skripting (XSS) zaifliklariga sabab boʻlishi mumkin. Oʻrniga [CORS](https://developer.mozilla.org/docs/Web/HTTP/CORS) bilan standart HTTP soʻrovlaridan foydalaning.

</docs-callout>

`withJsonpSupport`'ni kiritish `HttpClient`'da `.jsonp()` metodini yoqadi, bu metod maʼlumotlarni domenlararo yuklash uchun [JSONP konvensiyasi](https://en.wikipedia.org/wiki/JSONP) orqali GET soʻrovini yuboradi.

HELPFUL: Iloji boʻlsa, domenlararo soʻrovlar uchun JSONP oʻrniga [CORS](https://developer.mozilla.org/docs/Web/HTTP/CORS) dan foydalanishni afzal koʻring.

### `withXsrfConfiguration(...)`

Bu variantni kiritish `HttpClient`'ning oʻrnatilgan XSRF xavfsizlik funksiyasini sozlash imkonini beradi. Koʻproq maʼlumot uchun [xavfsizlik qoʻllanmasiga](best-practices/security) qarang.

### `withNoXsrfProtection()`

Bu variantni kiritish `HttpClient`'ning oʻrnatilgan XSRF xavfsizlik funksiyasini oʻchiradi. Koʻproq maʼlumot uchun [xavfsizlik qoʻllanmasiga](best-practices/security) qarang.

## `HttpClientModule`'ga asoslangan konfiguratsiya {#httpclientmodule-based-configuration}

Baʼzi ilovalar `HttpClient`'ni NgModule'larga asoslangan eski API yordamida sozlashi mumkin.

Bu jadvalda `@angular/common/http` dan mavjud NgModule'lar va ularning yuqoridagi provider konfiguratsiya funksiyalari bilan qanday bogʻliqligi keltirilgan.

| **NgModule**                            | `provideHttpClient()` ekvivalenti                         |
| --------------------------------------- | -------------------------------------------------------- |
| `HttpClientModule`                      | `provideHttpClient(withInterceptorsFromDi(), withXhr())` |
| `HttpClientJsonpModule` (eskirgan)      | `withJsonpSupport()` (eskirgan)                          |
| `HttpClientXsrfModule.withOptions(...)` | `withXsrfConfiguration(...)`                             |
| `HttpClientXsrfModule.disable()`        | `withNoXsrfProtection()`                                 |

NOTE: `HttpClientModule` va `HttpClientXsrfModule` ham eskirgan. Oʻrniga tegishli imkoniyatlar bilan `provideHttpClient`'dan foydalaning.

<docs-callout important title="HttpClientModule'ni bir nechta injector'da ishlatganda ehtiyot boʻling">
`HttpClientModule` bir nechta injector'da mavjud boʻlganda interceptor'larning xatti-harakati yomon aniqlangan boʻladi va aniq variantlar hamda provider/import tartibiga bogʻliq.

Koʻp injector'li konfiguratsiyalar uchun `provideHttpClient`'ni afzal koʻring, chunki uning xatti-harakati barqarorroq. Yuqoridagi `withRequestsMadeViaParent` imkoniyatiga qarang.
</docs-callout>
