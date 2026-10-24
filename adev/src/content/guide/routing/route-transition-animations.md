# Marshrut oʻtish animatsiyalari

Marshrut oʻtish animatsiyalari (route transition animations) Angular ilovangizdagi turli view'lar oʻrtasida harakatlanishda silliq vizual oʻtishlarni taʼminlab, foydalanuvchi tajribasini yaxshilaydi. [Angular Router](/guide/routing) brauzerning View Transitions API'sini oʻrnatilgan holda qoʻllab-quvvatlaydi va bu qoʻllab-quvvatlanadigan brauzerlarda marshrut oʻzgarishlari oʻrtasida uzluksiz animatsiyalarni amalga oshirish imkonini beradi.

## View Transitions qanday ishlaydi {#how-view-transitions-work}

View oʻtishlari ilovangizning turli holatlari oʻrtasida silliq animatsiyalar yaratish uchun brauzerning oʻrnatilgan [`document.startViewTransition` API](https://developer.mozilla.org/en-US/docs/Web/API/Document/startViewTransition)'sidan foydalanadi. API quyidagicha ishlaydi:

1. **Joriy holatni ushlab olish** — brauzer joriy sahifaning suratini oladi
2. **DOM yangilanishini bajarish** — DOM'ni yangilash uchun sizning callback funksiyangiz ishga tushadi
3. **Yangi holatni ushlab olish** — brauzer yangilangan sahifa holatini ushlab oladi
4. **Oʻtishni ijro etish** — brauzer eski va yangi holatlar oʻrtasida animatsiya qiladi

`startViewTransition` API'sining asosiy tuzilmasi quyidagicha:

```ts
document.startViewTransition(async () => {
  await updateTheDOMSomehow();
});
```

Brauzer API'si haqida batafsil maʼlumot uchun [Chrome Explainer](https://developer.chrome.com/docs/web-platform/view-transitions)'ga qarang.

## Router view oʻtishlaridan qanday foydalanadi {#how-the-router-uses-view-transitions}

Angular Router uzluksiz marshrut oʻzgarishlarini yaratish uchun view oʻtishlarini navigatsiya hayot sikliga integratsiya qiladi. Navigatsiya davomida Router:

1. **Navigatsiyaga tayyorgarlikni yakunlaydi** — marshrutlarni moslashtirish, [lazy loading](guide/routing/loading-strategies#lazily-loaded-components-and-routes), [himoyachilar](/guide/routing/route-guards), [resurslar](/guide/routing/data-fetching-with-resources) va [resolver'lar](/guide/routing/data-resolvers) bajariladi
2. **View oʻtishini boshlaydi** — marshrutlar faollashtirishga tayyor boʻlganda Router `startViewTransition`'ni chaqiradi
3. **DOM'ni yangilaydi** — Router oʻtish callback'i ichida yangi marshrutlarni faollashtiradi va eskilarini oʻchiradi
4. **Oʻtishni yakunlaydi** — Angular render qilishni tugatganda oʻtish Promise'i yechiladi (resolve)

Router'ning view oʻtishlari integratsiyasi [progressiv yaxshilash](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement) vazifasini bajaradi. Brauzerlar View Transitions API'sini qoʻllab-quvvatlamasa, Router animatsiyasiz oddiy DOM yangilanishlarini bajaradi va shu orqali ilovangiz barcha brauzerlarda ishlashini taʼminlaydi.

## Router'da View Transitions'ni yoqish {#enabling-view-transitions-in-the-router}

View oʻtishlarini [router konfiguratsiyangizga](/guide/routing/define-routes#adding-the-router-to-your-application) `withViewTransitions` imkoniyatini qoʻshish orqali yoqing. Angular standalone ham, NgModule bootstrap yondashuvini ham qoʻllab-quvvatlaydi:

### Standalone bootstrap {#standalone-bootstrap}

```ts
import {bootstrapApplication} from '@angular/platform-browser';
import {provideRouter, withViewTransitions} from '@angular/router';
import {routes} from './app.routes';

bootstrapApplication(MyApp, {
  providers: [provideRouter(routes, withViewTransitions())],
});
```

### NgModule bootstrap {#ngmodule-bootstrap}

```ts
import {NgModule} from '@angular/core';
import {RouterModule} from '@angular/router';

@NgModule({
  imports: [RouterModule.forRoot(routes, {enableViewTransitions: true})],
})
export class AppRouting {}
```

["count" misolini StackBlitz'da sinab koʻring](https://stackblitz.com/edit/stackblitz-starters-2dnvtm?file=src%2Fmain.ts)

Bu misol hisoblagich yangilanishlari uchun router navigatsiyasi toʻgʻridan-toʻgʻri `startViewTransition` chaqiruvlarini qanday almashtirishi mumkinligini koʻrsatadi.

## Oʻtishlarni CSS bilan sozlash {#customizing-transitions-with-css}

Noyob animatsiya effektlarini yaratish uchun view oʻtishlarini CSS yordamida sozlashingiz mumkin. Brauzer CSS selektorlari bilan moʻljalga olishingiz mumkin boʻlgan alohida oʻtish elementlarini yaratadi.

Maxsus oʻtishlar yaratish uchun:

1. **view-transition-name qoʻshing** — animatsiya qilmoqchi boʻlgan elementlarga noyob nomlar bering
2. **Global animatsiyalarni aniqlang** — global stillaringizda CSS animatsiyalarini yarating
3. **Oʻtish psevdo-elementlarini moʻljalga oling** — `::view-transition-old()` va `::view-transition-new()` selektorlaridan foydalaning

Quyida hisoblagich elementiga aylanish effektini qoʻshuvchi misol keltirilgan:

```css
/* Define keyframe animations */
@keyframes rotate-out {
  to {
    transform: rotate(90deg);
  }
}

@keyframes rotate-in {
  from {
    transform: rotate(-90deg);
  }
}

/* Target view transition pseudo-elements */
::view-transition-old(count),
::view-transition-new(count) {
  animation-duration: 200ms;
  animation-name: -ua-view-transition-fade-in, rotate-in;
}

::view-transition-old(count) {
  animation-name: -ua-view-transition-fade-out, rotate-out;
}
```

IMPORTANT: View oʻtish animatsiyalarini komponent stillarida emas, global stillar faylingizda aniqlang. Angular'ning [view inkapsulyatsiyasi](/guide/components/styling#style-scoping) komponent stillarini chegaralaydi va bu ularning oʻtish psevdo-elementlarini toʻgʻri moʻljalga olishiga toʻsqinlik qiladi.

[Yangilangan "count" misolini StackBlitz'da sinab koʻring](https://stackblitz.com/edit/stackblitz-starters-fwn4i7?file=src%2Fmain.ts)

## onViewTransitionCreated bilan oʻtishlarni ilgʻor boshqarish {#advanced-transition-control-with-onviewtransitioncreated}

`withViewTransitions` imkoniyati view oʻtishlarini ilgʻor boshqarish uchun `onViewTransitionCreated` callback'iga ega sozlamalar obyektini qabul qiladi. Bu callback:

- [Inyeksiya kontekstida](/guide/di/dependency-injection-context#run-within-an-injection-context) ishlaydi
- Quyidagilarni oʻz ichiga olgan [`ViewTransitionInfo`](/api/router/ViewTransitionInfo) obyektini qabul qiladi:
  - `startViewTransition`'dan olingan `ViewTransition` nusxasi
  - Qaysi marshrutdan oʻtilayotgani uchun [`ActivatedRouteSnapshot`](/api/router/ActivatedRouteSnapshot)
  - Qaysi marshrutga oʻtilayotgani uchun [`ActivatedRouteSnapshot`](/api/router/ActivatedRouteSnapshot)

Bu callback'dan navigatsiya kontekstiga qarab oʻtish xatti-harakatini sozlash uchun foydalaning. Masalan, muayyan navigatsiya turlari uchun oʻtishlarni oʻtkazib yuborishingiz mumkin:

```ts
import {inject} from '@angular/core';
import {Router, withViewTransitions, isActive, IsActiveMatchOptions} from '@angular/router';

withViewTransitions({
  onViewTransitionCreated: ({transition}) => {
    const router = inject(Router);
    const targetUrl = router.currentNavigation()!.finalUrl!;

    // Skip transition if only fragment or query params change
    const config: Partial<IsActiveMatchOptions> = {
      paths: 'exact',
      matrixParams: 'exact',
      fragment: 'ignored',
      queryParams: 'ignored',
    };

    const isTargetRouteCurrent = isActive(targetUrl, router, config);

    if (isTargetRouteCurrent()) {
      transition.skipTransition();
    }
  },
});
```

Bu misol navigatsiya faqat [URL fragmenti yoki soʻrov parametrlarini](/guide/routing/read-route-state#query-parameters) oʻzgartirganda (masalan, bir sahifa ichidagi anchor havolalar) view oʻtishini oʻtkazib yuboradi. `skipTransition()` metodi animatsiyani oldini oladi, lekin navigatsiyaning yakunlanishiga imkon beradi.

## Foydalanuvchining harakat sozlamalarini hurmat qilish {#respecting-the-users-motion-preferences}

Router foydalanuvchining [`prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) sozlamasidan qatʼi nazar view oʻtishlarini ishga tushiradi. Harakatni kamaytirish istagi foydalanuvchi umuman harakatni istamasligini anglatmaydi, shu sababli freymvork tanlovni ilovaga qoldiradi: bunday foydalanuvchilar uchun [yanada nozik animatsiyalar taqdim etishingiz](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#react_to_the_reduced_motion_preference) yoki `onViewTransitionCreated` callback'i bilan oʻtishni butunlay oʻtkazib yuborishingiz mumkin:

```ts
withViewTransitions({
  onViewTransitionCreated: ({transition}) => {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
      transition.skipTransition();
    }
  },
});
```

## Chrome explainer'idan Angular'ga moslashtirilgan misollar {#examples-from-the-chrome-explainer-adapted-to-angular}

Quyidagi misollar Chrome jamoasi hujjatlaridan Angular Router bilan ishlatish uchun moslashtirilgan turli view oʻtish texnikalarini koʻrsatadi:

### Oʻtuvchi elementlar bir xil DOM elementi boʻlishi shart emas {#transitioning-elements-dont-need-to-be-the-same-dom-element}

Elementlar bir xil `view-transition-name`'ga ega boʻlsa, turli DOM elementlari oʻrtasida silliq oʻtishi mumkin.

- [Chrome Explainer](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#transitioning_elements_dont_need_to_be_the_same_dom_element)
- [StackBlitz'dagi Angular misoli](https://stackblitz.com/edit/stackblitz-starters-dh8npr?file=src%2Fmain.ts)

### Maxsus kirish va chiqish animatsiyalari {#custom-entry-and-exit-animations}

Marshrut oʻtishlari davomida koʻrish maydoniga (viewport) kiruvchi va undan chiquvchi elementlar uchun noyob animatsiyalar yarating.

- [Chrome Explainer](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#custom_entry_and_exit_transitions)
- [StackBlitz'dagi Angular misoli](https://stackblitz.com/edit/stackblitz-starters-8kly3o)

### Asinxron DOM yangilanishlari va kontentni kutish {#async-dom-updates-and-waiting-for-content}

Angular Router qoʻshimcha kontent yuklanishini kutishdan koʻra darhol oʻtishlarni afzal koʻradi.

- [Chrome Explainer](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#async_dom_updates_and_waiting_for_content)

NOTE: Angular Router view oʻtishlarini kechiktirish usulini taqdim etmaydi. Bu dizayn qarori qoʻshimcha kontentni kutish davomida sahifalarning interaktiv boʻlmay qolishining oldini oladi. Chrome hujjatlarida qayd etilganidek: "Bu vaqt davomida sahifa muzlatilgan boʻladi, shu sababli bu yerdagi kechikishlar minimal darajada boʻlishi kerak… baʼzi hollarda kechikishdan butunlay qochib, sizda allaqachon mavjud kontentdan foydalanish yaxshiroq."

### View oʻtish turlari bilan bir nechta view oʻtish uslublarini boshqarish {#handle-multiple-view-transition-styles-with-view-transition-types}

Navigatsiya kontekstiga qarab turli animatsiya uslublarini qoʻllash uchun view oʻtish turlaridan foydalaning.

- [Chrome Explainer](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#view-transition-types)
- [StackBlitz'dagi Angular misoli](https://stackblitz.com/edit/stackblitz-starters-vxzcam)

### View oʻtish ildizidagi klass nomi bilan bir nechta view oʻtish uslublarini boshqarish (eskirgan) {#handle-multiple-view-transition-styles-with-a-class-name-on-the-view-transition-root-deprecated}

Bu yondashuv animatsiya uslublarini boshqarish uchun oʻtish ildiz elementidagi CSS klasslaridan foydalanadi.

- [Chrome Explainer](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#changing-on-navigation-type)
- [StackBlitz'dagi Angular misoli](https://stackblitz.com/edit/stackblitz-starters-nmnzzg?file=src%2Fmain.ts)

### Boshqa animatsiyalarni muzlatmasdan oʻtish {#transitioning-without-freezing-other-animations}

Yanada dinamik foydalanuvchi tajribasini yaratish uchun view oʻtishlari davomida sahifadagi boshqa animatsiyalarni davom ettiring.

- [Chrome Explainer](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#transitioning-without-freezing)
- [StackBlitz'dagi Angular misoli](https://stackblitz.com/edit/stackblitz-starters-76kgww)

### JavaScript bilan animatsiya qilish {#animating-with-javascript}

Murakkab animatsiya stsenariylari uchun JavaScript API'lari yordamida view oʻtishlarini dasturiy ravishda boshqaring.

- [Chrome Explainer](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#animating-with-javascript)
- [StackBlitz'dagi Angular misoli](https://stackblitz.com/edit/stackblitz-starters-cklnkm)
