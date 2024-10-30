import spacy
import re


class NLQueryParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            raise Exception("Please install spaCy model using: python -m spacy download en_core_web_sm")

        self.special_terms = {
            'more than': '>',
            'greater than': '>',
            'less than': '<',
            'at least': '>=',
            'at most': '<=',
            'equal to': '=',
            'in': 'IN',
            'not in': 'NOT IN'
        }

    def sanitize_value(self, value: str) -> str:
        """Sanitize input values to prevent SQL injection"""
        # Remove any dangerous characters
        return re.sub(r'[;\'"\\]', '', value)

    def parse_query(self, natural_query: str) -> str:
        doc = self.nlp(natural_query.lower())

        # Initialize query components
        select_clause = "SELECT e.*"
        from_clause = "FROM employees e"
        where_conditions = []
        join_clauses = []

        # Check for department information
        if 'department' in natural_query.lower():
            join_clauses.append("LEFT JOIN departments d ON e.department = d.name")

            # Look for department budget queries
            if 'budget' in natural_query.lower():
                select_clause = "SELECT e.name, e.department, d.budget"

        # Parse salary conditions
        salary_pattern = r"(?:salary|paid|earning|makes?).*?(\d+)[k\s]?"
        salary_matches = re.findall(salary_pattern, natural_query.lower())

        for match in salary_matches:
            amount = int(match) * 1000 if 'k' in match else int(match)

            # Determine comparison operator
            operator = '='
            for term, op in self.special_terms.items():
                if term in natural_query.lower():
                    operator = op
                    break

            where_conditions.append(f"e.salary {operator} {amount}")

        # Parse department specific queries
        dept_pattern = r"in\s+(\w+)\s+department"
        dept_matches = re.findall(dept_pattern, natural_query.lower())
        if dept_matches:
            department = self.sanitize_value(dept_matches[0].title())
            where_conditions.append(f"e.department = '{department}'")

        # Construct final query
        query_parts = [select_clause, from_clause]
        if join_clauses:
            query_parts.extend(join_clauses)
        if where_conditions:
            query_parts.append("WHERE " + " AND ".join(where_conditions))

        return " ".join(query_parts)