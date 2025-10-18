import random


pattern_messages_for_new_users = [
    "Keep checking in daily to unlock your personal patterns.",
    "Your patterns emerge through consistency — check in regularly to see them.",
    "Patterns reveal themselves with steady tracking — stay consistent.",
    "You’re close! A few more check-ins will uncover your mood patterns.",
    "Daily logs help us detect patterns — keep showing up.",
    "Consistency is the key to unlocking your emotional patterns.",
    "The more you check in, the clearer your patterns become.",
    "Patterns take shape with time — keep building your streak.",
    "Check in regularly to discover what influences your mood most.",
    "Unlock deeper insights by maintaining your check-in streak.",
    "A few consistent days are all it takes to start revealing patterns.",
    "Your next few check-ins could unlock meaningful patterns — keep going.",
    "Track consistently — each day adds a puzzle piece to your pattern map.",
    "Patterns don’t appear overnight. Stay consistent to uncover them.",
    "Daily entries build the foundation for pattern detection.",
    "Want to see your trends? Keep logging to unlock them.",
    "Regular check-ins help us surface your unique emotional patterns.",
    "Every day you log brings your mood pattern into sharper focus.",
    "Consistency = clarity. Check in daily to spot meaningful trends.",
    "You’ll unlock your mood patterns soon — stay consistent!"
]

mood_trend_messages_for_new_users = [
    "Keep checking in to unlock your mood trend insights.",
    "Mood trends appear when you log consistently — stay on track.",
    "Each check-in helps shape your mood trend — keep it going.",
    "Want to see your progress curve? Maintain your streak.",
    "Mood trends need consistent data — log daily to unlock them.",
    "Consistency creates clarity — keep checking in to reveal your trend.",
    "Every entry contributes to your long-term trend visualization.",
    "Check in each day to see how your moods evolve over time.",
    "Your mood trend grows with each log — don’t break the streak.",
    "Keep tracking to see your emotional trajectory come to life.",
    "Stay consistent — your mood trend unlocks with steady tracking.",
    "A few more check-ins and your mood trend will start to form.",
    "Your data builds your mood journey — keep it consistent.",
    "Each log adds to your emotional timeline — stay active.",
    "To understand your trend, maintain your check-in rhythm.",
    "Your next few entries will reveal how your mood shifts over time.",
    "The clearer your data, the stronger your mood trend insight.",
    "Momentum matters — keep logging to visualize your progress.",
    "Check in daily to watch your mood trend evolve naturally.",
    "Stay consistent — your trend story depends on it."
]



pattern_gap_messages = [
    "I noticed you haven’t checked in for {days} days — keep showing up to unlock your personal patterns.",
    "You’ve been away for {days} days — stay consistent to start seeing your emotional patterns again.",
    "It’s been {days} days since your last check-in. Your mood patterns grow clearer with consistency.",
    "{days} days without a log — your patterns pause when your entries do. Let’s restart today.",
    "Haven’t checked in for {days} days? Jump back in to rediscover your daily patterns.",
    "Your last check-in was {days} days ago — consistent tracking helps uncover your emotional rhythm.",
    "Looks like it’s been {days} days since your last check-in. Keep logging to see how your patterns evolve.",
    "You’re {days} days off your routine — consistent check-ins unlock meaningful insights.",
    "Missed {days} days? No worries. Let’s rebuild and get those patterns back on track.",
    "You’ve taken {days} days off — patterns emerge from steady reflection. Keep going."
]

mood_trend_gap_messages = [
    "It’s been {days} days since your last entry — regular tracking reveals your mood trend.",
    "After {days} days away, your trend paused — check in to start seeing progress again.",
    "{days} days gap detected — logging consistently helps chart your emotional growth.",
    "No entries for {days} days. Keep tracking daily to visualize your trend clearly.",
    "Your last check-in was {days} days ago — steady logs build accurate mood trends.",
    "{days} days since your last check-in — time to reconnect and rebuild your mood trend.",
    "Your mood trend fades with missed days. Let’s reset — it’s been {days} days since your last check-in.",
    "After {days} days, your trend needs fresh data — start logging again today.",
    "Missed {days} days? No big deal — consistent check-ins reveal your real trend over time.",
    "{days} days away — get back into the habit to bring your mood trend back to life."
]


def gap_messages( gap_days: int):
            """Return a random encouraging message based on the gap days."""
            gap_message = ""
            if 2 <= gap_days <= 3:
                gap_message = "short_gap_message"
            elif 4 <= gap_days <= 6:
                gap_message = "medium_gap_message"
            else:
                gap_message = "long_gap_message"
                
                
            gap_messages = {
                "short_gap_message": [
                                    "Glad to see you checking in again — even small gaps are part of the process.",
                                    "Nice to have you back today! Each day you log adds clarity to your patterns.",
                                    "Consistency matters more than perfection — thanks for showing up again.",
                                    "Today’s check-in helps keep the momentum going. Great job staying on track!",
                                    "Every entry counts. You’re building a strong habit one day at a time.",
                                    "Welcome back! Just a small gap — glad to see you again.",
                                    "Hey, just a quick pause — good to have you back checking in!",
                                    "You missed a day or two — no big deal, let's keep going.",
                                    "Nice to see you back so soon!",
                                    "Back after a quick break — love the consistency.",
                                    "Only a short pause — you're staying on track.",
                                    "Even with a small gap, you’re still building a great habit.",
                                    "You're keeping this habit alive — one day at a time.",
                                    "Just a tiny break — let's keep the streak strong.",
                                    "You’re still in a good rhythm — keep it up!",
                                    "Glad you came back quickly — consistency is key.",
                                    "Small breaks are normal — what matters is showing up again.",
                                    "Welcome back — you’re keeping the momentum going.",
                                    "Short break over — let’s get back into flow.",
                                    "You missed a check-in but bounced right back — well done.",
                                    "Quick pause — but your progress continues.",
                                    "Love the comeback — this is how habits stick.",
                                    "Back at it after a day or two — great job.",
                                    "Consistency is built just like this — even after a missed day.",
                                    "You're proving you can get back on track easily — keep going!"],
                "medium_gap_message": [
                                    "Good to see you after a short break — today’s check-in is a great reset.",
                                    "Nice job picking this back up — let’s build a little streak from here.",
                                    "Thanks for returning! Even after a few days off, you’re right back on track.",
                                    "This check-in reconnects your mood story. What’s shifted since last time?",
                                    "Great restart today — momentum is easier to rebuild than most people think.",
                                    "Welcome back! Taking a few days off is okay — good to see you here again.",
                                    "It's been a few days — great to have you checking in again.",
                                    "A few days away, but you're right back at it — that's what counts.",
                                    "You’re back after a short pause — this is how habits grow.",
                                    "Glad to see you picking this back up after a few days.",
                                    "Consistency isn’t about never missing — it’s about coming back. You did!",
                                    "A short break can be refreshing — let's see where you're at today.",
                                    "You're showing commitment by coming back after a few days away.",
                                    "You missed a few check-ins, but you’re here now — that’s progress.",
                                    "A short gap doesn’t erase your progress — glad you’re back.",
                                    "Welcome back! Let’s rebuild that rhythm together.",
                                    "Took a small breather — now let’s dive back in.",
                                    "You’re rejoining the habit loop — that’s huge.",
                                    "Gaps happen — your return means you care.",
                                    "Your check-in today keeps the habit alive — well done.",
                                    "Back after a few days — let's reset and keep going.",
                                    "A few days off gives a fresh perspective — great time to reflect.",
                                    "You’re proving to yourself you can restart anytime.",
                                    "Coming back after a gap is harder than starting — proud of you for doing it.",
                                    "This check-in is a great way to restart your streak."
                    ],
                "long_gap_message": [
                                    "Welcome back! It’s been a while — great to see you checking in again.",
                                    "You’ve been away for over a week, but this is the perfect day to restart.",
                                    "We’ve missed you here! Let’s make today the start of a fresh streak.",
                                    "Glad to have you back — the first check-in after a break is always powerful.",
                                    "It’s never too late to start again. Today’s entry matters more than you think.",
                                    "Welcome back! It’s been a while — today is a great day to restart.",
                                    "You've taken a longer break — glad you’re back to check in.",
                                    "It’s been a week or more — this is the perfect time to reset your flow.",
                                    "Glad to have you back after some time away — let’s make today count.",
                                    "Coming back after a longer gap takes effort — good job!",
                                    "Your return today is a fresh start — let’s build momentum again.",
                                    "It’s never too late to pick this back up — welcome back.",
                                    "This check-in is step one toward getting back into rhythm.",
                                    "Longer gaps happen — what matters is you came back today.",    
                                    "You’re pressing reset on your habit today — that’s powerful.",
                                    "It’s been a while — use today to reflect on what you need most right now.",
                                    "Coming back after a break shows real dedication — proud of you.",
                                    "You’re reactivating the habit — today is a turning point.",
                                    "Every comeback is a win — today is yours.",
                                    "This is a great opportunity to notice what’s changed since your last check-in.",
                                    "Welcome back — what’s one small thing you can do to support your energy today?",
                                    "A lot can happen in a week — today’s check-in matters.",
                                    "Glad you’re back — let’s get back to building momentum together.",
                                    "The fact that you came back after a long break shows you still care — keep going.",
                                    "This is your re-entry point — a chance to start fresh."
                    ],
            }
            
            return random.choice(gap_messages[gap_message])
            
