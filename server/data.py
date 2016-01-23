import os
import datetime
import markdown
from os.path import join as pjoin
import sys
DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(DIR)
from lib.yamllib import load
from importlib.machinery import SourceFileLoader

processor = markdown.Markdown(extensions=['mathjax'])

# def load(path):
#     with open(path) as f:
#         return yaml.load(f)

verdict_explanation = {
    'QU': 'in queue',
    'AC': 'accepted',
    'PE': 'presentation error',
    'WA': 'wrong answer',
    'CE': 'compile time error',
    'RE': 'runtime error',
    'TL': 'time limit exceeded',
    'ML': 'memory limit exceeded',
    'OL': 'output limit exceeded',
    'SE': 'submission error',
    'RF': 'restricted function',
    'CJ': 'cannot judge',
}


def read(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return None

class Team:
    def __init__(self, name, title, password, location, groups):
        self.name = name
        self.title = title
        self.password = password
        self.location = location
        self.groups = groups
        self.last_used_language = None

    @staticmethod
    def load_all(path):
        teams = []
        data = load(pjoin(path, 'teams.yml'))
        groups = data['groups']

        for name, d in data['teams'].items():
            teams.append(Team(
                name=name,
                title=d.get('title', name),
                password=d['pass'],
                location=d.get('location', 'unknown'),
                groups=set(d.get('groups', [])),
            ))

        return teams, groups


class Judge:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    @staticmethod
    def load_all(path):
        judges = []
        data = load(pjoin(path, 'judges.yml'))

        for name, d in data.items():
            judges.append(Judge(
                name=name,
                password=d['pass'],
            ))

        return judges


class Problem:
    def __init__(self, id, title, points, problem, statement, assets):
        self.id = id
        self.title = title
        self.points = points
        self.statement = statement
        self.assets = assets
        self.problem = problem
        self.problem_module = SourceFileLoader("problem." + self.id, self.problem).load_module()
        self._grader = self.problem_module.grade

    def __repr__(self):
        return '<Problem %s>' % repr(self.title)

    def score(self, answer):
        return self._grader(answer)

    @staticmethod
    def load(path, id):
        path = os.path.abspath(path)

        problem = load(path)

        statement = pjoin(os.path.dirname(path), 'statement', 'index.html')

        assert os.path.isfile(statement)

        with open(statement, encoding='utf-8') as f:
            statement = f.read()

        dpath = os.path.dirname(path)
        if os.path.isdir(pjoin(dpath, 'assets')):
            assets = pjoin(dpath, 'assets')
        elif os.path.isdir(pjoin(dpath, 'statement')):
            assets = pjoin(dpath, 'statement')
        else:
            assets = None

        return Problem(
            id=id,
            title=problem['title'],
            points=problem['points'],
            problem=pjoin(dpath, 'problem.py'),
            statement=statement,
            assets=assets,
        )

    @staticmethod
    def load_all(path):
        problems = []
        problem_dir = pjoin(path, 'problems')
        for p in os.listdir(problem_dir):
            if p.endswith('.yml'):
                problems.append(Problem.load(pjoin(problem_dir, p), os.path.splitext(p)[0]))
            elif os.path.isfile(pjoin(problem_dir, p, 'problem.yml')):
                problems.append(Problem.load(pjoin(problem_dir, p, 'problem.yml'), p))
            elif os.path.isfile(pjoin(problem_dir, p, '.epsilon', 'problem.yml')):
                problems.append(Problem.load(pjoin(problem_dir, p, '.epsilon', 'problem.yml'), p))
        return problems


class Phase:
    def __init__(self, contest, start, status, countdown, visible_problems, submit_problems, scoreboard_problems, problem_list, frozen):
        self.contest = contest
        self.start = start
        self.status = status
        self.countdown = countdown
        self.visible_problems = visible_problems
        self.submit_problems = submit_problems
        self.scoreboard_problems = scoreboard_problems
        self.problem_list = problem_list
        self.frozen = frozen

    def current_countdown(self):
        if self.countdown is None:
            return None
        return 60.0 * self.countdown - (self.contest.time_elapsed() - 60.0 * self.start)

    def frozen_time(self):
        if self.frozen is None:
            return None
        return self.contest.start + datetime.timedelta(seconds=self.frozen * 60)

    @staticmethod
    def load(contest, start, d):

        visible_problems = set()
        submit_problems = set()
        scoreboard_problems = []
        problem_list = []

        for problem in d.get('problems', []):

            if type(problem) is str:
                problem_list.append(('text', problem))
            else:
                assert len(problem) == 1

                for k, v in problem.items():
                    pid = k
                    opts = v

                if 'visible' in opts:
                    visible_problems.add(pid)
                    problem_list.append(('problem', pid))

                if 'submit' in opts:
                    submit_problems.add(pid)
                if 'scoreboard' in opts:
                    scoreboard_problems.append(pid)

        return Phase(
            contest=contest,
            start=start,
            status=d.get('status', None),
            countdown=d.get('countdown', None),
            visible_problems=visible_problems,
            submit_problems=submit_problems,
            scoreboard_problems=scoreboard_problems,
            problem_list=problem_list,
            frozen=d.get('frozen', None),
        )


class Contest:
    BEFORE_START = 0
    RUNNING = 1
    FINISHED = 2

    def __init__(self, id, title, db, start, duration, teams, problems, phases, groups, judges, register=False):
        self.id = id
        self.title = title
        self.db = db
        self.start = start
        self.duration = duration
        self.teams = teams
        self.problems = problems
        self.phases = phases
        self.groups = groups
        self.register = register
        self.judges = judges

    def time_elapsed(self):
        return (datetime.datetime.now() - self.start).total_seconds()

    def time_remaining(self):
        return self.time_total() - self.time_elapsed()

    def time_total(self):
        return 60.0 * self.duration

    def time_to_start(self):
        return (self.start - datetime.datetime.now()).total_seconds()

    def second_format(self, s):
        return (self.start + datetime.timedelta(seconds=s))

    def status(self):
        if self.time_remaining() < 0:
            return Contest.FINISHED
        if self.time_elapsed() >= 0:
            return Contest.RUNNING
        return Contest.BEFORE_START

    def get_current_phase(self):
        now = self.time_elapsed()
        res = Phase.load(self, None, {})
        for k, v in self.phases:
            if now < 60.0 * k:
                break
            res = v
        return res

    @staticmethod
    def load(path):
        contest = load(pjoin(path, 'contest.yml'))
        teams, groups = Team.load_all(path)
        judges = Judge.load_all(path)
        res = Contest(
            id=contest['id'],
            title=contest['title'],
            db=contest['db'],
            start=contest['start'],
            duration=contest['duration'],
            teams={team.name: team for team in teams},
            groups=groups,
            problems={problem.id: problem for problem in Problem.load_all(path)},
            phases=None,
            judges={judge.name: judge for judge in judges},
            register=contest.get('register', False),
        )

        res.phases = [(k, Phase.load(res, k, v)) for k, v in sorted(contest['phases'].items())]
        return res


class ScoreboardTeamProblem:
    def __init__(self):
        self.solved_at = None
        self.try_count = 0
        self.new_submissions = 0
        self._score = 0
        self._points = 0
        self.current_count = 0

    def submit(self, at, score, points):
        if score > self._score:
            self.solved_at = at
            self._score = score
            self._points = points
            self.try_count += self.current_count
        else:
            self.current_count += 1

    def submit_new(self):
        if self.solved_at is None:
            self.new_submissions += 1

    def score(self):
        return self._score

    def points(self):
        return self._points

    def is_solved(self):
        return self.score()>0

    def time_penalty(self):
        if not self.is_solved():
            return 0
        return self.solved_at + self.try_count * 5.0 * 60.0


class Balloon:
    def __init__(self, id, submission, team, problem, delivered):
        self.id = id
        self.submission = submission
        self.team = team
        self.problem = problem
        self.delivered = delivered
