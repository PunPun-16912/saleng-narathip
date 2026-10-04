# tasks.md | รายการงานย่อยสำหรับ SPEC-ROUTE

- Feature: การรับงานตามเส้นทาง (ซาเล้ง)
- Spec ID: specs/002-route/spec.md
- อ้างอิง plan.md: specs/002-route/plan.md
- วันที่: 2026-10-04
- สรุป: 8 task ทั้งหมด, 0 task ที่ยังรอ Q-xx หลังจากทีมตัดสินใจ stack และโยงกับ spec แล้ว, และทีมได้เลือก stack แบบชัดเจน: React + Vite + Tailwind, FastAPI, PostgreSQL

## T-01 ตั้งโครงโปรเจกต์และสิ่งจำเป็นสำหรับ route feature
- รองรับ: REQ-FN-002, REQ-QA-002, REQ-CON-002
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tailwind.config.js`, `frontend/src/`, `backend/app/main.py`, `backend/requirements.txt`, `backend/app/api/`, `backend/app/services/`, `db/init.sql`, `tests/`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: รัน test เปล่าผ่าน 1 ตัวและโครงโปรเจกต์พร้อมรองรับ feature route ตาม stack React + Vite + Tailwind, FastAPI, PostgreSQL
- สถานะ: เสร็จ รอทีมตรวจ

## T-02 สร้างแบบจำลองข้อมูลและสถานะคำขอสำหรับงานรับซื้อ
- รองรับ: REQ-FN-001, REQ-FN-002, REQ-BR-002, REQ-SEC-002, SC-04, REQ-PRV-001, REQ-PRV-002
- ตรวจด้วย: AC-04-04, AC-04-05, AC-04-08
- ไฟล์ที่แตะ: `models/scrapRequest.ts`, `models/location.ts`, `models/verification.ts`, `types/route.ts`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: model สำหรับงาน, ตำแหน่ง, สถานะงาน, และเหตุการณ์ยืนยันตัวตนพร้อมใช้งานและตรงตามกำหนดข้อมูล
- สถานะ: เสร็จ รอทีมตรวจ

## T-03 สร้าง service คัดกรองและเรียงลำดับงานตามเส้นทางจริง
- รองรับ: REQ-FN-002, REQ-OP-002, REQ-QA-002, REQ-CON-002, AS-03
- ตรวจด้วย: AC-04-01, AC-04-02, AC-04-03, AC-04-06, AC-04-07
- ไฟล์ที่แตะ: `services/routeFilter.ts`, `services/routing.ts`, `services/locationAccuracy.ts`
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: ระบบสามารถกรองงานที่อยู่ภายในรัศมี 5 กม. ตาม route distance และจัดเรียงตามความใกล้เคียงของเส้นทางจริง
- สถานะ: เสร็จ รอทีมตรวจ

## T-04 สร้าง API ดึงรายการงานและอัปเดตตำแหน่งซาเล้ง
- รองรับ: REQ-FN-002, REQ-OP-002, REQ-QA-002, REQ-CON-002, AS-03
- ตรวจด้วย: AC-04-01, AC-04-06, AC-04-07
- ไฟล์ที่แตะ: `api/routeJobs.ts`, `api/location.ts`, `controllers/route.controller.ts`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: API คืนรายการงานตามเส้นทางจริงให้ซาเล้งภายใต้ความแม่นยำและเวลาตอบกลับที่กำหนด และรับอัปเดตตำแหน่งซาเล้งได้
- สถานะ: เสร็จ รอทีมตรวจ

## T-05 เพิ่มกลไกป้องกัน concurrent accept แบบ First-come
- รองรับ: REQ-BR-002, AS-02, REQ-CON-003
- ตรวจด้วย: AC-04-05
- ไฟล์ที่แตะ: `services/acceptJob.ts`, `repositories/jobRepository.ts`, `validators/acceptValidator.ts`
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: เมื่อมีซาเล้ง 2 คนกดรับงานพร้อมกัน ระบบให้สิทธิ์คนที่ Request ถึง Server ก่อนเท่านั้น และไม่อนุญาตการรับซ้ำ
- สถานะ: เสร็จ รอทีมตรวจ

## T-06 ปรับ flow ซ่อนพิกัดและยืนยันตัวตนก่อนเปิดเผยข้อมูลเต็ม
- รองรับ: REQ-SEC-002, SC-04, REQ-PRV-001, REQ-PRV-002, AS-04
- ตรวจด้วย: AC-04-08
- ไฟล์ที่แตะ: `services/privacyMask.ts`, `services/verification.ts`, `api/verification.ts`, `ui/addressMask.ts`
- ต้องทำหลัง: T-02, T-05
- เสร็จเมื่อ: พิกัดบ้านเลขที่ถูกซ่อนจนกว่าซาเล้งกดรับงานและยืนยันตัวตนแล้วเท่านั้น และข้อมูล PII ถูกปกป้องตามข้อกำหนด
- สถานะ: เสร็จ รอทีมตรวจ

## T-07 สร้างหน้าจอรายการงานตามเส้นทางและกระบวนการรับงาน
- รองรับ: REQ-FN-001, REQ-FN-002, REQ-BR-002, REQ-SEC-002, REQ-QA-002
- ตรวจด้วย: AC-04-03, AC-04-04, AC-04-05, AC-04-08
- ไฟล์ที่แตะ: `ui/RouteJobsPage.tsx`, `ui/JobCard.tsx`, `ui/AcceptJobButton.tsx`, `mocks/routeApi.ts`
- ต้องทำหลัง: ไม่มี (หน้าจอใช้ API จำลองก่อน)
- เสร็จเมื่อ: หน้าแสดงรายการงานตามเส้นทางแบบเรียงตามเส้นทางจริง, แสดงราคากลางและใช้คอนเทนต์ปกปิดจนกว่าจะยืนยันตัวตนแล้ว
- สถานะ: เสร็จ รอทีมตรวจ

## T-08 ทดสอบ end-to-end และประเมิน NFR ตาม acceptance criteria
- รองรับ: REQ-FN-002, REQ-BR-002, REQ-OP-002, REQ-QA-002, REQ-SEC-002
- ตรวจด้วย: AC-04-01 ถึง AC-04-08
- ไฟล์ที่แตะ: `tests/route.acceptance.test.ts`, `tests/route.performance.test.ts`, `tests/route.privacy.test.ts`
- ต้องทำหลัง: T-03, T-04, T-05, T-06, T-07
- เสร็จเมื่อ: test สำหรับทุก AC ผ่าน และตัวชี้วัด latency, accuracy, และ privacy ครอบคลุมเงื่อนไข NFR ตาม spec
- สถานะ: เสร็จ รอทีมตรวจ

## ตารางตรวจความครบ: AC -> task
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-04-01 | T-03, T-04, T-08 |
| AC-04-02 | T-03, T-08 |
| AC-04-03 | T-03, T-07, T-08 |
| AC-04-04 | T-02, T-07, T-08 |
| AC-04-05 | T-05, T-07, T-08 |
| AC-04-06 | T-03, T-04, T-08 |
| AC-04-07 | T-03, T-04, T-08 |
| AC-04-08 | T-06, T-07, T-08 |

## ตารางตรวจความครบ: Constraint -> task
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| REQ-CON-002 | T-01, T-03, T-04 |
| REQ-CON-003 | T-05 |
| SC-04 | T-02, T-06 |
| REQ-PRV-001 | T-02, T-06 |
| REQ-PRV-002 | T-02, T-06 |
| AS-02 | T-05 |
| AS-03 | T-03, T-04 |
| AS-04 | T-06, T-07 |
| AS-05 | T-03, T-08 |
| AS-06 | T-04, T-08 |

## สิ่งที่ยังไม่ทำ
- Q-01: กรณีซาเล้ง 2 คนกดรับงานพร้อมกันในเสี้ยววินาทีเดียวกัน — task ที่เกี่ยวข้องคือ T-05, T-08 และยังต้องยืนยันคำตอบจากทีมก่อนจัดการกันอย่างถาวร
- Q-02: ควรคำนวณ “5 กม.” จากระยะทางตรงหรือเส้นทางจริงที่ซาเล้งจะเดินทาง — task ที่เกี่ยวข้องคือ T-03, T-04 และยังต้องยืนยันจาก Product / GIS ก่อนเริ่มทำจริง
- Q-03: การยืนยันตัวตน Thai-ID / DBD-ID จะเกิดก่อนหรือหลังรับงาน — task ที่เกี่ยวข้องคือ T-06 และยังต้องยืนยันจาก Product / Compliance ก่อนพัฒนาถึง step สุดท้าย
- Q-04: “ภายใน <= 3 วินาที” ต้องวัดจากจุดไหนและเงื่อนไขใด — task ที่เกี่ยวข้องคือ T-04, T-08 และยังต้องมีการตกลงเงื่อนไขการทดสอบก่อนทำค่า benchmark ที่จริงจัง
