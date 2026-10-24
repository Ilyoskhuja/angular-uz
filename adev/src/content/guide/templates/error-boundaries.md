# `@boundary` bilan xato chegaralari

IMPORTANT: `@boundary` [developer preview](reference/releases#developer-preview) bosqichida.

Angular shablonlari render qilish va oʻzgarishlarni aniqlash davomida yuzaga keladigan runtime xatolarni muloyim tarzda qayta ishlash uchun xato chegaralarini (error boundaries) qoʻllab-quvvatlaydi.

Xato chegaralari bitta komponentdagi nosozlik butun ilovani ishdan chiqarishining oldini oladi va foydalanuvchiga zaxira (fallback) UI koʻrsatish imkonini beradi.

## `@boundary` va `@error` bilan xatolarni ushlash {#catching-errors-with-boundary-and-error}

`@boundary` bloki shabloningizning bir qismini oʻrab oladi. Agar bu chegara ichidagi har qanday komponent yoki direktiva initsializatsiya yoki oʻzgarishlarni aniqlash davomida xato tashlasa, freymvork xatoni ushlab oladi va uning oʻrniga `@error` blokini render qiladi.

```angular-html
@boundary {
  <app-risky-component />
} @error {
  <p>Something went wrong!</p>
}
```

## Xato obyektiga murojaat qilish {#accessing-the-error-object}

Ushlangan xatoga yashirin (implicit) `$error` oʻzgaruvchisi orqali murojaat qilishingiz mumkin:

```angular-html
@boundary {
  <app-risky-component />
} @error {
  <p>Error occurred: {{ $error.message }}</p>
}
```

## Chegarani qayta tiklash {#resetting-the-boundary}

`@error` blokida yashirin `$reset` funksiyasini chaqirib, `@boundary` kontentini qayta render qilishga urinib koʻrishingiz mumkin. Chaqirilganda u chegara holatini qayta tiklaydi va asl kontentni yana render qilishga harakat qiladi.

```angular-html
@boundary {
  <app-flaky-component />
} @error {
  <p>Loading failed.</p>
  <button (click)="$reset()">Try again</button>
}
```

## `when` bilan shartli xatolarni qayta ishlash {#conditional-error-handling-with-when}

Xatolarning maʼlum turlarini shartli qayta ishlash va turli zaxira UI'lar taqdim etish uchun `when` shartlaridan foydalanishingiz mumkin. Angular bu shartni xatoni ushlaganda hisoblaydi.

```angular-html
@boundary {
  <app-chart-dashboard />
} @error (let err; reset = $reset; when isRenderError(err)) {
  <p>Network issue. Check your connection.</p>
  <button (click)="reset()">Retry</button>
} @error {
  <p>An unexpected error occurred: {{ $error.message }}</p>
}
```

`@error` bloklaringizni eng aniqdan eng umumiyga tartiblang, chunki Angular `when` shartlarini tartib bilan hisoblaydi va true qiymat beradigan birinchisini ishlatadi. `when` shartisiz yakuniy `@error` bloki barcha qolgan xatolarni ushlovchi zaxira variant vazifasini bajaradi.

## Global xato ishlov beruvchisi bilan integratsiya {#global-error-handler-integration}

Chegara xatoni ushlaganda Angular global `ErrorHandler`'ni ham xabardor qilishi mumkin. Ushlangan bu xatolarni xato kuzatish servisingizga yozib qoʻyish uchun maxsus `ErrorHandler`'ingizda ixtiyoriy `onViewError` hook'ini amalga oshirishingiz mumkin.

```ts
@Injectable()
export class MyErrorHandler implements ErrorHandler {
  handleError(error: any): void {
    // Handle uncaught errors
  }

  onViewError(error: Error, details: ErrorDetails): void {
    // Handle errors caught by a @boundary
    console.warn('Caught by boundary:', details.boundary);
    myErrorTrackingService.log(error);
  }
}
```

IMPORTANT: Agar `@error` blokining oʻzi xato tashlasa, xato keyingi tashqi `@boundary`'ga uzatiladi yoki Angular uni qayta ishlanmagan ilova xatosi sifatida koʻradi.

## Kontent proyeksiyasi {#content-projection}

Agar komponentingiz [kontent proyeksiyasidan](guide/components/content-projection) foydalansa, `<ng-content>`'ni `@boundary`'ga oʻrash proyeksiya qilingan kontentdagi xatolarni ushlamaydi. Bu kontent uni eʼlon qilgan view'ga tegishli, qabul qiluvchi komponentning view'iga emas.

Masalan, quyidagi shablonga ega oʻram komponenti unga proyeksiya qilingan komponentlardagi xatolarni ushlamaydi:

```angular-html {avoid}
@boundary {
  <ng-content />
} @error {
  <p>Something went wrong!</p>
}
```

Bu xatolarni ushlash uchun ota shablonda oʻram komponentini va uning proyeksiya qilingan kontentini `@boundary`'ga oʻrang:

```angular-html {prefer}
@boundary {
  <app-wrapper>
    <app-risky-component />
  </app-wrapper>
} @error {
  <p>Something went wrong!</p>
}
```

## Dinamik view'lar va dasturiy xatolarni qayta ishlash {#dynamic-views-and-programmatic-error-handling}

Xatolarni qayta ishlash shablon sintaksisi bilan cheklanmagan. Agar komponentlar yoki oʻrnatilgan view'larni (embedded views) dinamik ravishda yaratayotgan boʻlsangiz, xatolarni qayta ishlash uchun `onError` opsiyasidan foydalanishingiz mumkin. Koʻproq maʼlumot uchun dasturiy render qilish qoʻllanmasidagi [Render qilish xatolarini qayta ishlash](guide/components/programmatic-rendering#handling-rendering-errors) boʻlimiga qarang.
