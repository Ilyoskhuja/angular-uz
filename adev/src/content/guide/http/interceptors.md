# Interceptor'lar

`HttpClient` _interceptor'lar_ deb nomlanuvchi middleware shaklini qoʻllab-quvvatlaydi.

TLDR: Interceptor'lar — bu qayta urinish (retry), keshlash, jurnalga yozish (logging) va autentifikatsiya kabi umumiy patternlarni alohida soʻrovlardan ajratib, abstraksiya qilish imkonini beruvchi middleware.

`HttpClient` ikki turdagi interceptor'larni qoʻllab-quvvatlaydi: funksional va DI'ga asoslangan. Bizning tavsiyamiz — funksional interceptor'lardan foydalanish, chunki ularning xatti-harakati, ayniqsa murakkab konfiguratsiyalarda, yanada oldindan aytib boʻladigan. Bu qoʻllanmadagi misollarimiz funksional interceptor'lardan foydalanadi, [DI'ga asoslangan interceptor'larni](#di-based-interceptors) esa oxirida alohida boʻlimda yoritamiz.

## Interceptor'lar {#interceptors}

Interceptor'lar odatda har bir soʻrov uchun ishga tushirishingiz mumkin boʻlgan funksiyalar boʻlib, soʻrov va javoblarning mazmuni va umumiy oqimiga taʼsir qilish uchun keng imkoniyatlarga ega. Siz bir nechta interceptor oʻrnatishingiz mumkin, ular interceptor zanjirini hosil qiladi va har bir interceptor soʻrov yoki javobni zanjirdagi keyingi interceptor'ga uzatishdan oldin qayta ishlaydi.

Interceptor'lardan turli umumiy patternlarni amalga oshirish uchun foydalanishingiz mumkin, masalan:

- Muayyan API'ga chiquvchi soʻrovlarga autentifikatsiya sarlavhalarini qoʻshish.
- Muvaffaqiyatsiz soʻrovlarni eksponensial kechikish (exponential backoff) bilan qayta urinish.
- Javoblarni maʼlum vaqt davomida yoki oʻzgartirishlar tomonidan bekor qilinmaguncha keshlash.
- Javoblarni tahlil qilishni sozlash.
- Server javob vaqtlarini oʻlchash va ularni jurnalga yozish.
- Tarmoq operatsiyalari bajarilayotganda yuklanish spinneri kabi UI elementlarini boshqarish.
- Maʼlum vaqt oraligʻida yuborilgan soʻrovlarni toʻplash va guruhlash (batching).
- Sozlanadigan muddat yoki timeout'dan keyin soʻrovlarni avtomatik muvaffaqiyatsiz deb hisoblash.
- Serverni muntazam soʻrab turish (polling) va natijalarni yangilash.

## Interceptor'ni aniqlash {#defining-an-interceptor}

Interceptor'ning asosiy shakli — chiquvchi `HttpRequest`'ni va interceptor zanjiridagi keyingi qayta ishlash qadamini ifodalovchi `next` funksiyasini qabul qiluvchi funksiya.

Masalan, bu `loggingInterceptor` soʻrovni uzatishdan oldin chiquvchi soʻrov URL'ini `console.log`'ga yozadi:

```ts
export function loggingInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  console.log(req.url);
  return next(req);
}
```

Bu interceptor soʻrovlarni haqiqatda ushlab qolishi uchun `HttpClient`'ni undan foydalanishga sozlashingiz shart.

## Interceptor'larni sozlash {#configuring-interceptors}

Foydalaniladigan interceptor'lar toʻplamini `HttpClient`'ni bogʻliqliklarni inyeksiya qilish orqali sozlashda `withInterceptors` imkoniyati yordamida eʼlon qilasiz:

```ts
bootstrapApplication(App, {
  providers: [provideHttpClient(withInterceptors([loggingInterceptor, cachingInterceptor]))],
});
```

Siz sozlagan interceptor'lar provider'larda keltirgan tartibingizda zanjirga ulanadi. Yuqoridagi misolda `loggingInterceptor` soʻrovni qayta ishlab, soʻngra uni `cachingInterceptor`'ga uzatadi.

### Javob hodisalarini ushlab qolish {#intercepting-response-events}

Interceptor javobga murojaat qilish yoki uni oʻzgartirish uchun `next` qaytargan `HttpEvent`'larning `Observable` oqimini transformatsiya qilishi mumkin. Bu oqim barcha javob hodisalarini oʻz ichiga olgani uchun, yakuniy javob obyektini aniqlash uchun har bir hodisaning `.type`'ini tekshirish zarur boʻlishi mumkin.

```ts
export function loggingInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  return next(req).pipe(
    tap((event) => {
      if (event.type === HttpEventType.Response) {
        console.log(req.url, 'returned a response with status', event.status);
      }
    }),
  );
}
```

TIP: Interceptor'lar javoblarni oʻzlarining chiquvchi soʻrovlari bilan tabiiy ravishda bogʻlaydi, chunki ular javob oqimini soʻrov obyektini qamrab olgan closure ichida transformatsiya qiladi.

## Soʻrovlarni oʻzgartirish {#modifying-requests}

`HttpRequest` va `HttpResponse` nusxalarining koʻpgina jihatlari _oʻzgarmas_ (immutable) va interceptor'lar ularni bevosita oʻzgartira olmaydi. Oʻrniga interceptor'lar bu obyektlarni `.clone()` operatsiyasi yordamida klonlab va yangi nusxada qaysi xususiyatlar oʻzgartirilishi kerakligini koʻrsatib oʻzgarishlarni qoʻllaydi. Bu qiymatning oʻzida (masalan, `HttpHeaders` yoki `HttpParams`) oʻzgarmas yangilanishlarni bajarishni oʻz ichiga olishi mumkin.

Masalan, soʻrovga sarlavha qoʻshish uchun:

```ts
const reqWithHeader = req.clone({
  headers: req.headers.set('X-New-Header', 'new header value'),
});
```

Bu oʻzgarmaslik bir xil `HttpRequest` interceptor zanjiriga bir necha marta yuborilganda koʻpgina interceptor'larning idempotent boʻlishiga imkon beradi. Bu bir qancha sabablarga koʻra, jumladan soʻrov muvaffaqiyatsizlikdan keyin qayta urinilganda sodir boʻlishi mumkin.

CRITICAL: Soʻrov yoki javobning tanasi (body) chuqur oʻzgarishlardan himoyalanmagan **emas**. Agar interceptor tanani oʻzgartirishi kerak boʻlsa, bir xil soʻrovda bir necha marta ishga tushishini hisobga olishga eʼtibor bering.

## Interceptor'larda bogʻliqliklarni inyeksiya qilish {#dependency-injection-in-interceptors}

Interceptor'lar ularni roʻyxatdan oʻtkazgan injector'ning _inyeksiya kontekstida_ ishga tushadi va bogʻliqliklarni olish uchun Angular'ning [`inject`](/api/core/inject) API'sidan foydalanishi mumkin.

Masalan, ilovada chiquvchi soʻrovlar uchun autentifikatsiya tokenlarini yaratuvchi `AuthService` nomli servis bor deb faraz qilaylik. Interceptor bu servisni inyeksiya qilib, undan foydalanishi mumkin:

```ts
export function authInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn) {
  // Inject the current `AuthService` and use it to get an authentication token:
  const authToken = inject(AuthService).getAuthToken();

  // Clone the request to add the authentication header.
  const newReq = req.clone({
    headers: req.headers.append('X-Authentication-Token', authToken),
  });
  return next(newReq);
}
```

## Soʻrov va javob metamaʼlumotlari {#request-and-response-metadata}

Koʻpincha soʻrovga backend'ga yuborilmaydigan, lekin aynan interceptor'lar uchun moʻljallangan maʼlumotni kiritish foydali boʻladi. `HttpRequest`'lar bunday metamaʼlumotlarni `HttpContext` nusxasi sifatida saqlovchi `.context` obyektiga ega. Bu obyekt kalitlari `HttpContextToken` turida boʻlgan tiplangan map sifatida ishlaydi.

Bu tizim qanday ishlashini koʻrsatish uchun muayyan soʻrov uchun keshlash interceptor'i yoqilganligini boshqarishda metamaʼlumotlardan foydalanamiz.

### Kontekst tokenlarini aniqlash {#defining-context-tokens}

Keshlash interceptor'i muayyan soʻrovni keshlashi kerakligini oʻsha soʻrovning `.context` map'ida saqlash uchun kalit vazifasini bajaradigan yangi `HttpContextToken` aniqlang:

```ts
export const CACHING_ENABLED = new HttpContextToken<boolean>(() => true);
```

Berilgan funksiya token uchun qiymat aniq oʻrnatilmagan soʻrovlar uchun tokenning standart qiymatini yaratadi. Funksiyadan foydalanish token qiymati obyekt yoki massiv boʻlsa, har bir soʻrov oʻz nusxasini olishini taʼminlaydi.

### Tokenni interceptor'da oʻqish {#reading-the-token-in-an-interceptor}

Soʻngra interceptor tokenni oʻqib, uning qiymatiga qarab keshlash mantigʻini qoʻllash yoki qoʻllamaslikni tanlashi mumkin:

```ts
export function cachingInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  if (req.context.get(CACHING_ENABLED)) {
    // apply caching logic
    return ...;
  } else {
    // caching has been disabled for this request
    return next(req);
  }
}
```

### Soʻrov yuborishda kontekst tokenlarini oʻrnatish {#setting-context-tokens-when-making-a-request}

`HttpClient` API orqali soʻrov yuborishda `HttpContextToken`'lar uchun qiymatlar berishingiz mumkin:

```ts
const data$ = http.get('/sensitive/data', {
  context: new HttpContext().set(CACHING_ENABLED, false),
});
```

Interceptor'lar bu qiymatlarni soʻrovning `HttpContext`'idan oʻqishi mumkin.

### Soʻrov konteksti oʻzgaruvchan {#the-request-context-is-mutable}

`HttpRequest`'larning boshqa xususiyatlaridan farqli oʻlaroq, bogʻlangan `HttpContext` _oʻzgaruvchan_ (mutable). Agar interceptor keyinroq qayta uriniladigan soʻrovning kontekstini oʻzgartirsa, oʻsha interceptor qayta ishga tushganda kontekst oʻzgarishini koʻradi. Bu zarur boʻlsa holatni bir nechta qayta urinishlar boʻylab uzatish uchun foydali.

## Sintetik javoblar {#synthetic-responses}

Koʻpgina interceptor'lar soʻrov yoki javobni transformatsiya qilib, shunchaki `next` ishlov beruvchisini chaqiradi, lekin bu qatʼiy talab emas. Bu boʻlimda interceptor murakkabroq xatti-harakatni qamrab olishi mumkin boʻlgan bir nechta yoʻllar muhokama qilinadi.

Interceptor'lar `next`'ni chaqirishi shart emas. Ular oʻrniga javoblarni boshqa mexanizm orqali, masalan, keshdan yoki soʻrovni muqobil mexanizm orqali yuborish yoʻli bilan tuzishni tanlashi mumkin.

Javobni `HttpResponse` konstruktori yordamida tuzish mumkin:

```ts
const resp = new HttpResponse({
  body: 'response body',
});
```

## Yoʻnaltirish maʼlumotlari bilan ishlash {#working-with-redirect-information}

`HttpClient` fetch backend'idan foydalanganda javoblar javob yoʻnaltirish (redirect) natijasi boʻlganligini koʻrsatuvchi `redirected` xususiyatini oʻz ichiga oladi. Bu xususiyat native Fetch API spetsifikatsiyasiga mos keladi va interceptor'larda yoʻnaltirish holatlarini qayta ishlash uchun foydali boʻlishi mumkin.

Interceptor yoʻnaltirish maʼlumotlariga murojaat qilib, ular asosida harakat qilishi mumkin:

```ts
export function redirectTrackingInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  return next(req).pipe(
    tap((event) => {
      if (event.type === HttpEventType.Response && event.redirected) {
        console.log('Request to', req.url, 'was redirected to', event.url);
        // Handle redirect logic - maybe update analytics, security checks, etc.
      }
    }),
  );
}
```

Yoʻnaltirish maʼlumotlaridan interceptor'laringizda shartli mantiqni amalga oshirish uchun ham foydalanishingiz mumkin:

```ts
export function authRedirectInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  return next(req).pipe(
    tap((event) => {
      if (event.type === HttpEventType.Response && event.redirected) {
        // Check if we were redirected to a login page
        if (event.url?.includes('/login')) {
          // Handle authentication redirect
          handleAuthRedirect();
        }
      }
    }),
  );
}
```

## Javob turlari bilan ishlash {#working-with-response-types}

`HttpClient` fetch backend'idan foydalanganda javoblar brauzer javobni CORS siyosatlari va soʻrov rejimiga qarab qanday qayta ishlaganini koʻrsatuvchi `responseType` xususiyatini oʻz ichiga oladi. Bu xususiyat native Fetch API spetsifikatsiyasiga mos keladi va CORS muammolarini tuzatish hamda javobning qanchalik ochiq ekanligini tushunish uchun qimmatli maʼlumot beradi.

Javobning `responseType` xususiyati quyidagi qiymatlarga ega boʻlishi mumkin:

- `'basic'` - Barcha sarlavhalari ochiq same-origin javob
- `'cors'` - CORS sarlavhalari toʻgʻri sozlangan cross-origin javob
- `'opaque'` - CORS'siz cross-origin javob, sarlavhalar va tana cheklangan boʻlishi mumkin
- `'opaqueredirect'` - no-cors rejimida yoʻnaltirilgan soʻrovdan kelgan javob
- `'error'` - Tarmoq xatosi yuz berdi

Interceptor javob turi maʼlumotlaridan CORS'ni tuzatish va xatolarni qayta ishlash uchun foydalanishi mumkin:

```ts
export function responseTypeInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
  return next(req).pipe(
    tap((event) => {
      if (event.type === HttpEventType.Response) {
        // Handle different response types appropriately
        switch (event.responseType) {
          case 'opaque':
            // Limited access to response data
            console.warn('Limited response data due to CORS policy');
            break;
          case 'cors':
          case 'basic':
            // Full access to response data
            break;
          case 'error':
            // Handle network errors
            console.error('Network error in response');
            break;
        }
      }
    }),
  );
}
```

## DI'ga asoslangan interceptor'lar {#di-based-interceptors}

`HttpClient` shuningdek inyeksiya qilinadigan klasslar sifatida aniqlangan va DI tizimi orqali sozlangan interceptor'larni ham qoʻllab-quvvatlaydi. DI'ga asoslangan interceptor'larning imkoniyatlari funksional interceptor'lar bilan bir xil, lekin sozlash mexanizmi boshqacha.

DI'ga asoslangan interceptor — bu `HttpInterceptor` interfeysini implementatsiya qiluvchi inyeksiya qilinadigan klass:

```ts
@Injectable()
export class LoggingInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, handler: HttpHandler): Observable<HttpEvent<any>> {
    console.log('Request URL: ' + req.url);
    return handler.handle(req);
  }
}
```

DI'ga asoslangan interceptor'lar bogʻliqliklarni inyeksiya qilish multi-provider'i orqali sozlanadi:

```ts
bootstrapApplication(App, {
  providers: [
    provideHttpClient(
      // DI-based interceptors must be explicitly enabled.
      withInterceptorsFromDi(),
    ),

    {provide: HTTP_INTERCEPTORS, useClass: LoggingInterceptor, multi: true},
  ],
});
```

DI'ga asoslangan interceptor'lar provider'lari roʻyxatdan oʻtkazilgan tartibda ishga tushadi. Keng va ierarxik DI konfiguratsiyasiga ega ilovada bu tartibni oldindan aytish juda qiyin boʻlishi mumkin.
