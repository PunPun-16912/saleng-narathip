# prompt-log.md บันทึกการใช้ AI ของกลุ่ม <ชื่อกลุ่ม>

กติกา: เพิ่มต่อท้ายเท่านั้น ห้ามแก้หรือลบบันทึกเดิม
ทุกบันทึกมี: เลขที่ | วันที่ | เครื่องมือ | คำสั่ง | สิ่งที่ AI ถามหรือรายงาน | คำตอบหรือการตัดสินใจของทีม | สิ่งที่ AI เดา (ถ้ามี)
AI จะเพิ่มบันทึกให้เองเมื่อใช้คำสั่ง /clarify /plan /tasks /implement ทีมเพิ่มเองได้เมื่อสั่งแก้นอกคำสั่ง

## #1 | 2026-10-04 | Copilot | /clarify specs/002-rute/spec.md
- AI ถาม: 
  - กรณีซาเล้ง 2 คนกดรับงานพร้อมกัน ระบบใช้กติกาใด
  - ควรคำนวณรัศมี 5 กม. จากระยะทางตรงหรือเส้นทางจริงที่ซาเล้งจะเดินทาง
  - พิกัดบ้านเลขที่ผู้ขายต้องซ่อนไว้จนกว่าจะมีการรับงานหรือไม่
  - ความคลาดเคลื่อน GPS ต้องวัดจากอะไร
  - เวลา <= 3 วินาที ต้องวัดจากจุดไหน
  - การยืนยันตัวตนต้องเกิดก่อนหรือหลังการรับงาน
- คำตอบหรือการตัดสินใจของทีม: ใช้ First-come สำหรับกรณีกดรับงานพร้อมกัน; คำนวณความใกล้ชิดตามเส้นทางจริงที่ซาเล้งจะเดินทาง; ซ่อนพิกัดละเอียดจนกว่าซาเล้งกดรับงานและยืนยันตัวตน; ใช้ accuracy ของอุปกรณ์ร่วมกับค่าแปลผลระยะทางสำหรับความคลาดเคลื่อน GPS; วัดเวลา response ของ API ที่ฝั่ง Backend สำหรับข้อมูลในรัศมี 5 กม.; ให้ยืนยันตัวตนก่อนเปิดเผยพิกัดละเอียดและก่อนอนุมัติรับงาน
- สิ่งที่ AI เดา: ใช้ระยะทางตรงสำหรับคำนวณรัศมี 5 กม. หากไม่มีคำตอบ และใช้ First-come ตาม request ที่ถึง server ก่อน

## #2 | 2026-10-04 | Copilot | /clarify specs/002-route/spec.md
- AI ตรวจสอบและกำหนดว่า spec มีความกำกวมด้านการคำนวณระยะทาง, การจัดการ concurrent accept, การซ่อนข้อมูล, และการวัด NFR
- คำตอบหรือการตัดสินใจของทีม: จัดทำเป็น assumptions ใหม่ใน spec.md เพื่อยืนยันแนวทาง First-come และ route distance ตามการเดินทางจริง
- สิ่งที่ AI แก้: ปรับ status เป็น Draft v2, ปรับคำอธิบาย REQ-FN-002, และเพิ่ม AS-02 ถึง AS-06 ในหัวข้อ Open Questions & Assumptions

## #3 | 2026-10-04 | Copilot | /plan specs/002-route/spec.md
- AI ตรวจสอบและสร้าง plan.md จาก spec.md พร้อมตารางตรวจ constraints และ traceability ไปยัง REQ/AC
- คำตอบหรือการตัดสินใจของทีม: ใช้แนวทางแบบ draft v2 โดยคำนึงถึง route distance, First-come, และ masking address จนกว่าจะยืนยันตัวตน
- สิ่งที่ AI สร้าง: ไฟล์ plan.md ที่ /workspaces/saleng-narathip/specs/002-route/plan.md พร้อมตาราง constraints, model, API, test plan, และ open issues

## #4 | 2026-10-04 | Copilot | /tasks specs/002-route/spec.md
- AI ตรวจสอบ spec.md และ plan.md แล้วแยกงานเป็น task ตามลำดับการพึ่งพาและพร้อมทดสอบ AC ที่เกี่ยวข้อง
- คำตอบหรือการตัดสินใจของทีม: ใช้ไดนามิกแบบก้าวหน้า โดยเว้น task ที่ต้องรอ Open Questions ไว้เป็นสถานะ รอ Q-xx และระบุ task ที่สามารถเริ่มทำทันที
- สิ่งที่ AI สร้าง: ไฟล์ tasks.md ที่ /workspaces/saleng-narathip/specs/002-route/tasks.md พร้อมตารางตรวจความครบของ AC และ Constraint

## #5 | 2026-10-04 | ทีม | ปรับ stack ให้ตรงกับทางเลือกของทีม
- AI รายงาน: stack เดิมยังวางไว้เป็น “ยังไม่ได้เลือก” ซึ่งไม่สอดคล้องกับความต้องการจริงของทีม
- คำตอบหรือการตัดสินใจของทีม: เลือก Frontend เป็น React + Vite + Tailwind CSS, Backend เป็น FastAPI, Database เป็น PostgreSQL
- สิ่งที่ AI แก้: ปรับ [specs/002-route/spec.md](/workspaces/saleng-narathip/specs/002-route/spec.md), [specs/002-route/plan.md](/workspaces/saleng-narathip/specs/002-route/plan.md), และ [specs/002-route/tasks.md](/workspaces/saleng-narathip/specs/002-route/tasks.md) ให้สอดคล้องกับ stack ที่เลือก โดยคงชื่อตัวแปรและ ID เดิมตาม spec

## #6 | 2026-10-04 | Copilot | /implement T-01 specs/002-route/tasks.md
- AI ตรวจสอบ task T-01 ว่าเป็นงานพื้นฐานของโครงสร้างโปรเจกต์และมีสถานะ "พร้อมทำ" จึงเริ่มสร้างเฉพาะไฟล์ที่ระบุในช่อง "ไฟล์ที่แตะ"
- ไฟล์ที่สร้างหรือแก้: `frontend/package.json`, `frontend/vite.config.js`, `frontend/tailwind.config.js`, `frontend/postcss.config.js`, `frontend/index.html`, `frontend/src/main.jsx`, `frontend/src/App.jsx`, `frontend/src/index.css`, `backend/app/__init__.py`, `backend/app/main.py`, `backend/requirements.txt`, `db/init.sql`, `tests/test_route_structure.py`
- ผล test: `npm run build --silent` ใน `frontend` ผ่านและ `PYTHONPATH=. pytest tests/test_route_structure.py -q` ผ่าน 2 test
- สิ่งที่ AI เกือบต้องเดา: ไม่มี เพราะ task นี้ไม่มีการคาดเดาสิ่งที่ไม่ระบุใน spec และไม่ได้ข้าม Open Question อย่างใด

## #7 | 2026-10-04 | Copilot | /implement tasks/002-route/tasks.md
- AI ดำเนินการ implement ทั้งหมดตาม tasks.md โดยไม่ข้ามช่วงต้องทำและยึดตาม stack ที่เลือก: React + Vite + Tailwind, FastAPI, PostgreSQL
- ไฟล์ที่สร้างหรือแก้: `frontend/src/data/mockJobs.js`, `frontend/src/components/JobCard.jsx`, `frontend/src/pages/RouteJobsPage.jsx`, `frontend/src/App.jsx`, `backend/app/main.py`, `tests/test_route_feature.py`
- ผล test: `PYTHONPATH=. pytest tests/test_route_feature.py -q` ผ่าน 5 test และ `cd frontend && npm run build --silent` ผ่าน
- สิ่งที่ AI เกือบต้องเดา: ไม่มี เนื่องจากแรงกดดันจาก spec และ plan ชัดเจนว่าต้องใช้ route distance, First-come, และ masking address จึงเลือกทำตาม assumptions ที่ยืนยันแล้วโดยชัดเจน

